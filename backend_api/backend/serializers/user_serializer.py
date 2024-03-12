from rest_framework import serializers

from . import UserTypeSerializer
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'password_hash']
        read_only_fields = ['id']
