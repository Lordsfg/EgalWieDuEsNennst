from rest_framework import serializers

from .item_serializer import ItemSerializer
from .user_serializer import UserSerializer
from .item_history_type_serializer import ItemHistoryTypeSerializer
from .room_serializer import RoomSerializer
from ..models import ItemHistory, Item, User, ItemHistoryType, Room


class ItemHistorySerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    item_history_type = serializers.PrimaryKeyRelatedField(queryset=ItemHistoryType.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = ItemHistory
        fields = ['id', 'item', 'user', 'item_history_type', 'room', 'date']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Override the default to_representation method to nest the user_type field.
        """
        representation = super().to_representation(instance)
        representation['item'] = ItemSerializer(instance.item).data
        representation['user'] = UserSerializer(instance.user).data
        representation['item_history_type'] = ItemHistoryTypeSerializer(instance.item_history_type).data
        representation['room'] = RoomSerializer(instance.room).data
        return representation
