import factory
from faker import Faker
fake = Faker()

import party.models as models


class PartyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Party

    description = fake.text()
    date = fake.date_between()


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SpareItem

    party = factory.SubFactory(PartyFactory)
    item_name = factory.Faker('email')
    total_price = 10


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Member

    party = factory.SubFactory(PartyFactory)
    name = factory.Faker('first_name')
    money_spent = 2


class SharePartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SharePart

    member = factory.SubFactory(MemberFactory)
    item = factory.SubFactory(ItemFactory)
    share = 0.2
