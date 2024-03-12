from .base_view import BaseCRUDAPIView
from ..serializers import UserSerializer
from ..models import User


class UserView(BaseCRUDAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = {'id': 'id', 'first_name': 'first_name', 'last_name': 'last_name', 'email': 'email', 'user_type': 'user_type'}
