from .base_view import BaseCRUDAPIView
from ..serializers import ItemHistorySerializer
from ..models import ItemHistory


class ItemHistoryView(BaseCRUDAPIView):
    queryset = ItemHistory.objects.all()
    serializer_class = ItemHistorySerializer
    lookup_fields = {'id': 'id', 'item': 'item', 'user': 'user', 'item_history_type': 'item_history_type', 'room': 'room', 'date': 'date'}
