from .base_view import BaseCRUDAPIView
from ..serializers import ItemHistoryTypeSerializer
from ..models import ItemHistoryType


class ItemHistoryTypeView(BaseCRUDAPIView):
    queryset = ItemHistoryType.objects.all()
    serializer_class = ItemHistoryTypeSerializer
    lookup_fields = {'id': 'id', 'name': 'name'}