from rest_framework import serializers

from . import ProductTypeSerializer, RoomSerializer, UserSerializer
from ..models import Item, ProductType, Room, User


class ItemSerializer(serializers.ModelSerializer):
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())
    current_room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    borrowed_by_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Item
        fields = ['id', 'product_type', 'current_room', 'annotation', 'borrowed_by_user', 'qr_code']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Override the default to_representation method to nest the user_type field.
        """
        representation = super().to_representation(instance)
        representation['product_type'] = ProductTypeSerializer(instance.product_type).data
        representation['current_room'] = RoomSerializer(instance.current_room).data
        representation['borrowed_by_user'] = UserSerializer(instance.borrowed_by_user).data
        return representation

