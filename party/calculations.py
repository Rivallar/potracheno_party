from django.db.models import F, Sum, FloatField, ExpressionWrapper
from party.models import Member, SharePart, Exchange


def calculate(party):

    """Main report function. Checks the input data and calculates who pays whom for a party."""

    members = Member.objects.filter(party=party)

    # Checking input data
    shares_missing = check_shares(members)
    diff = check_money_spent(members, party)

    if shares_missing or diff > 5:
        return f'Check your input, something went wrong.\nDelta: {diff},\n{shares_missing}'

    # Forming initial members balances (diff between money paid and how much consumed)
    members_dict, bills = get_initial_balances(members)

    # Figuring out who pays whom to make zero balance (paid = consumed)
    while len(bills) and ((bills[0] < 0) and (bills[-1] > 0)):
        who_pays_who(members_dict, bills, party)


def find_name(bill, members_dict):

    """Find a key of a dict by its value"""

    for key, val in members_dict.items():
        if val == bill:
            return key


def cleanup_zeros(members_dict, bills):

    """Removes zero balance from bills and zero-balance member from members_dict as he owes nobody and
    nobody owes him anymore."""

    members_dict_copy = members_dict.copy()
    for key, value in members_dict_copy.items():
        if 0 <= value < 0.00000001:
            del members_dict[key]

    bills_copy = bills.copy()
    for i in bills_copy:
        if 0 <= i < 0.00000001:
            bills.remove(i)


def member_report(member, in_detail=False):

    """Returns a money balance (diff) between money paid and money consumed or
    detailed report with each spare item consumed with its share."""

    spared = member.money_spent
    base_q = SharePart.objects.filter(member=member).prefetch_related('item').annotate(
        member_price=ExpressionWrapper(F('item__total_price') * F('share'), output_field=FloatField()))
    consumed_items = base_q.values_list('item__item_name', 'item__total_price', 'share', 'member_price')
    consumed_price = base_q.aggregate(total=Sum('member_price'))['total']
    balance = float(spared) - consumed_price

    if in_detail:   # Detailed report as a string

        report = f'{member.name}\n'
        for item in consumed_items:
            report += f'{item}\n'
        report += f'Заплатил: {spared}\n'
        report += f'Пожрал на: {consumed_price}\n'
        report += f'Баланс: {balance}'

        return report

    else:
        return {member: balance}


def check_shares(members):

    """Checks if each spare item of a party has its shares filled up to 100%.
    Returns a dict of items with shares filled less than 100%."""

    shares = SharePart.objects.filter(member__in=members).values_list('item__item_name').annotate(total=Sum('share'))
    shares_missing = {}
    for item in shares:
        if item[1] < 0.99:
            shares_missing[item[0]] = round(item[1], 2)
    return shares_missing


def check_money_spent(members, party):

    """Compares sums of money spent by all members and cost of all spare items."""

    members_money = members.aggregate(total=Sum('money_spent'))['total']
    items_sum = party.items.all().aggregate(total=Sum('total_price'))['total']
    diff = abs(members_money - items_sum)
    return diff


def get_initial_balances(members):

    """Computes the balance (difference between money paid and money consumed) for all party members.
    Returns a dict and an ordered list of balances."""

    members_dict = {}
    bills = []
    for member in members:
        members_bill = member_report(member)
        bill_value = list(members_bill.values())[0]
        if bill_value != 0:
            members_dict.update(members_bill)
            bills.append(bill_value)
    bills.sort()

    return members_dict, bills


def who_pays_who(members_dict, bills, party):

    """Takes the biggest positive and negative balances. One pays another, so someone`s balance turns into zero.
    Cleans zero-balance member from a list and reorders it again."""

    giver_val = bills[0]
    giver = find_name(giver_val, members_dict)
    taker_val = bills[-1]
    taker = find_name(taker_val, members_dict)

    if abs(giver_val) > abs(taker_val):
        money = taker_val               # lowest balance pays the highest balance until the highest becomes zero
    else:
        money = abs(giver_val)          # lowest balance pays the highest balance until the lowest becomes zero

    Exchange.objects.create(party=party, giver=giver, taker=taker, amount=money)

    members_dict[taker] -= money
    members_dict[giver] += money
    bills[0] += money
    bills[-1] -= money

    cleanup_zeros(members_dict, bills)
    bills.sort()


def party_money_spent(party):

    """Calculates how much money was spent for a party based on sum of its items prices."""

    total = party.items.all().aggregate(total=Sum('total_price'))['total']
    if total:
        return round(total, 2)
    return 0
