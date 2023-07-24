import pytest

from party.models import Party


@pytest.mark.django_db
def test_party_deletion(create_party):
    party = create_party
    assert Party.objects.count() == 1
    party.delete()
    assert Party.objects.count() == 1
    assert Party.objects.last().is_active is False
    party.delete(is_soft=False)
    assert Party.objects.count() == 0


@pytest.mark.django_db
def test_save_sharepart(prepare_share_parts, share_part_factory):
    item, member1, member2 = prepare_share_parts
    share_part_factory.create(item=item, member=member1, share=2)
    assert item.members.count() == 0
    share_part_factory.create(item=item, member=member1, share=0.5)
    assert item.members.count() == 1
    share_part_factory.create(item=item, member=member2, share=2)
    assert item.members.count() == 1
    share_part_factory.create(item=item, member=member2, share=0.3)
    assert item.members.count() == 2
