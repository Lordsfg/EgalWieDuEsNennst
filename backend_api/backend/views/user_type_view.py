from .base_view import BaseCRUDAPIView
from ..serializers import UserTypeSerializer
from ..models import UserType


class UserTypeView(BaseCRUDAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    lookup_fields = {'id': 'id', 'name': 'name'}
