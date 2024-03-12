from rest_framework import serializers

from . import UserTypeSerializer
from ..models import User, UserType


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'password_hash']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Override the default to_representation method to nest the user_type field.
        """
        representation = super().to_representation(instance)
        representation['user_type'] = UserTypeSerializer(instance.user_type).data
        return representation
