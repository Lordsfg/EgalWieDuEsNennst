from rest_framework import serializers

from . import ProductTypeSerializer, RoomSerializer, UserSerializer
from ..models import Item, ProductType, Room, User


class ItemSerializer(serializers.ModelSerializer):
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())
    current_room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    borrowed_by_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

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

        if representation['borrowed_by_user'] is None or representation['borrowed_by_user'].get('id') is None:
            del representation['borrowed_by_user']
        return representation

class ItemReturnModel(serializers.ModelSerializer):

    ## user infos
    user_id = serializers.IntegerField(source='borrowed_by_user.id', required=False)
    user_name = serializers.CharField(source='borrowed_by_user.first_name', required=False)
    user_type = serializers.CharField(source='borrowed_by_user.user_type.name', required=False)
    user_email = serializers.CharField(source='borrowed_by_user.email', required=False)

    ## items metadata that is in another table
    item_name = serializers.CharField(source='product_type.name', required=False)
    description = serializers.CharField(source='product_type.description', required=False)
    location = serializers.CharField(source='current_room.room_number', required=False)

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'description', 'annotation', 'location', 'user_id', 'user_name', 'user_type', 'user_email']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Override the default to_representation method to format the output.
        """
        representation = super().to_representation(instance)

        ## include user infos if given
        borrowed_by_user = instance.borrowed_by_user
        if borrowed_by_user:
            representation['user_id'] = borrowed_by_user.id
            representation['user_name'] = f"{borrowed_by_user.first_name} {borrowed_by_user.last_name}"
            representation['user_type'] = borrowed_by_user.user_type.name
        else:
            # Remove user_id and user_name if item is not borrowed by any user
            representation.pop('user_id', None)
            representation.pop('user_name', None)
            representation.pop('user_type', None)
        return representation
    