import pytest

from party.calculations import find_name, cleanup_zeros, check_shares, check_money_spent, member_report,\
    get_initial_balances, who_pays_who, calculate, party_money_spent
from party.models import Exchange


def test_find_name():
    members_dict = {'aaa': 30, 'bbb': 15, 'ccc': 8}
    bill = 15
    assert find_name(bill, members_dict) == 'bbb'


def test_cleanup_zeros():
    members_dict = {'a': 45, 'b': 56, 'c': 0, 'd': 13, 'e': 0.0000000001}
    bills = [0, 13, 56, 45, 0.0000000001]
    cleanup_zeros(members_dict, bills)
    assert len(bills) == 3
    assert list(members_dict.keys()) == ['a', 'b', 'd']


def test_check_shares(prepare_check_shares):
    members = prepare_check_shares
    missing = check_shares(members)
    assert len(missing) == 1
    assert list(missing.values())[0] == 0.6


def test_check_money_spent(prepare_check_shares):
    members = prepare_check_shares
    party = members[0].party
    diff = check_money_spent(members, party)
    assert diff == 10


def test_member_report(prepare_check_shares):
    members = prepare_check_shares
    report = member_report(members[4])
    assert list(report.values())[0] == 0
    report = member_report(members[0], in_detail=True)
    assert report.endswith('Баланс: -2.0')


def test_get_initial_balances(prepare_check_shares):
    members = prepare_check_shares
    members_dict, bills = get_initial_balances(members)
    assert len(members_dict) == len(bills) == 3
    assert set(bills) == {-2}


def test_who_pays_who(prepare_bills):
    members_dict, bills, party = prepare_bills
    giver = find_name(-5, members_dict)
    who_pays_who(members_dict, bills, party)
    assert Exchange.objects.count() == 1
    exchange = Exchange.objects.last()
    assert exchange.giver == giver
    assert exchange.amount == 5
    assert len(bills) == 2
    assert max(bills) == 5


def test_calculate(small_party_setup):
    party, members = small_party_setup
    calculate(party)
    assert Exchange.objects.count() == 2
    assert Exchange.objects.get(giver=members[0]).amount == 5
    assert Exchange.objects.get(giver=members[1]).amount == 2


def test_party_money_spent(create_party, small_party_setup):
    empty_party = create_party
    party, members = small_party_setup
    assert party_money_spent(empty_party) == 0
    assert party_money_spent(party) == 20
