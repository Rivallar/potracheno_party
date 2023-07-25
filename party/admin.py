from django.contrib import admin
from django.db.models import Sum

from .models import SpareItem, Member, SharePart, Party, Exchange
from party.calculations import party_money_spent


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['description', 'date', 'participants', 'money_spent']

    def participants(self, obj):
        return list(obj.members.all())

    def money_spent(self, obj):
        return party_money_spent(obj)


@admin.register(Member)
class AdminMember(admin.ModelAdmin):
    list_display = ['party', 'name', 'money_spent', 'pays_for']

    def pays_for(self, obj):
        return list(obj.spares.all().values_list('item_name', flat=True))


def assign_consumers(modeladmin, request, queryset):
    members = Member.objects.all()
    share = 1 / len(members)
    for obj in queryset:
        consumers = obj.members.all()
        for member in members:
            if member not in consumers:
                SharePart.objects.create(member=member, item=obj, share=share)


assign_consumers.short_description = 'Assign ALL as consumers'


@admin.register(SpareItem)
class AdminSpareItem(admin.ModelAdmin):
    list_display = ('item_name', 'party', 'total_price', 'who_consumes', 'parts')
    actions = [assign_consumers]

    def who_consumes(self, obj):
        return list(obj.members.all())

    def parts(self, obj):
        parts = SharePart.objects.filter(item=obj).aggregate(total=Sum('share'))['total']
        if parts:
            return round(parts, 2)
        return 0


@admin.register(SharePart)
class AdminSpareParts(admin.ModelAdmin):
    list_display = ['item', 'member', 'share']


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['party', 'giver', 'taker', 'amount']
