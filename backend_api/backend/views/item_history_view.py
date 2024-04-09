from .base_view import BaseCRUDAPIView
from ..serializers import ItemHistorySerializer
from ..models import ItemHistory
from rest_framework import status
from rest_framework.response import Response

class ItemHistoryView(BaseCRUDAPIView):
    queryset = ItemHistory.objects.all()
    serializer_class = ItemHistorySerializer
    lookup_fields = {'id': 'id', 'item': 'item', 'user': 'user', 'item_history_type': 'item_history_type', 'room': 'room', 'date': 'date'}
    


class GetItemHistoryByItemId(BaseCRUDAPIView):
    queryset = ItemHistory.objects.all()
    serializer_class = ItemHistorySerializer
    def get(self, request, id):
        item_history = ItemHistory.objects.filter(item__id=id)
        serializer = ItemHistorySerializer(item_history, many=True)
        return Response(serializer.data)