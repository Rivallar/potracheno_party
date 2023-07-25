from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PartyListSerializer, PartyDetailSerializer, ItemSerializer, MemberReportSerializer
from .models import Party, Member


class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Party.objects.filter(is_active=True)
    serializer_class = PartyListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartyDetailSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['get'], serializer_class=ItemSerializer)
    def items(self, request, *args, **kwargs):
        party = self.get_object()
        items = party.items.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class MemberReportViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Member.objects.all()
    serializer_class = MemberReportSerializer