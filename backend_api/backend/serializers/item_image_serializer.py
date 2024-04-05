from rest_framework import serializers
from ..models import ItemImage

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'file_name', 'device_id']