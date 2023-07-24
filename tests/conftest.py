import pytest
from pytest_factoryboy import register
from tests.factories import PartyFactory, ItemFactory, MemberFactory, SharePartFactory


register(PartyFactory)
register(ItemFactory)
register(MemberFactory)
register(SharePartFactory)


@pytest.fixture
def create_party(db, party_factory):
    party = party_factory.create()
    return party


@pytest.fixture
def prepare_share_parts(db, item_factory, member_factory):
    item = item_factory.create()
    member1 = member_factory.create(party=item.party)
    member2 = member_factory.create(party=item.party, name='aaa')
    return item, member1, member2


@pytest.fixture
def prepare_check_shares(db, item_factory, share_part_factory, member_factory):
    item1 = item_factory.create()
    party = item1.party
    members_list = [member_factory(party=party) for _ in range(5)]
    for member in members_list:
        share_part_factory.create(item=item1, member=member)

    item2 = item_factory.create(party=item1.party)
    for member in members_list[:-2]:
        share_part_factory.create(item=item2, member=member)

    members = party.members.all()

    return members


@pytest.fixture
def prepare_bills(db, party_factory, member_factory):
    party = party_factory.create()
    members = []
    members_dict = {}
    bills = []
    for i in [0, 5, 10, 15]:
        members.append(member_factory.create(party=party, money_spent=1))
    for n, i in enumerate([-5, -2, 0, 10]):
        members_dict[members[n]] = i
        bills.append(i)
    return members_dict, bills, party


@pytest.fixture
def small_party_setup(db, party_factory, member_factory, item_factory, share_part_factory):
    party = party_factory()
    members = []
    for i in [0, 5, 15]:
        members.append(member_factory.create(party=party, money_spent=i))

    items = []
    for i in [4, 6, 10]:
        items.append(item_factory.create(party=party, total_price=i))

    share_part_factory.create(item=items[0], member=members[0], share=0.5)
    share_part_factory.create(item=items[0], member=members[1], share=0.5)

    share_part_factory.create(item=items[1], member=members[0], share=0.333333333333)
    share_part_factory.create(item=items[1], member=members[1], share=0.333333333333)
    share_part_factory.create(item=items[1], member=members[2], share=0.333333333333)

    share_part_factory.create(item=items[2], member=members[0], share=0.1)
    share_part_factory.create(item=items[2], member=members[1], share=0.3)
    share_part_factory.create(item=items[2], member=members[2], share=0.6)

    return party, members
