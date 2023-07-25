from rest_framework import serializers
from party.models import Party, Member, Exchange, SpareItem, SharePart
from party.calculations import party_money_spent, member_report


class PartyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('id', 'description', 'date')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'money_spent')


class MemberReportSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Member
        fields = ('id', 'name', 'party', 'money_spent', 'report')

    def get_report(self, obj):
        return member_report(obj, in_detail=True)


class ExchangeSerializer(serializers.ModelSerializer):
    giver = serializers.SerializerMethodField(read_only=True)
    taker = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Exchange
        fields = ('giver', 'amount', 'taker')

    def get_giver(self, obj):
        return obj.giver.name

    def get_taker(self, obj):
        return obj.taker.name


class PartyDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    exchanges = ExchangeSerializer(many=True)
    total_spent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'description', 'date', 'total_spent', 'members', 'exchanges')

    def get_total_spent(self, obj):
        return party_money_spent(obj)


class SharePartSerializer(serializers.ModelSerializer):

    member_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SharePart
        fields = ('member', 'member_name', 'share')

    def get_member_name(self, obj):
        return obj.member.name


class ItemSerializer(serializers.ModelSerializer):
    parts = SharePartSerializer(many=True)

    class Meta:
        model = SpareItem
        fields = ('item_name', 'total_price', 'count', 'one_item_price', 'parts')