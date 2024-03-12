from .base_view import BaseCRUDAPIView
from ..serializers import ProductTypeSerializer
from ..models import ProductType


class ProductTypeView(BaseCRUDAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    lookup_fields = {'id': 'id', 'name': 'name', 'description': 'description'}
