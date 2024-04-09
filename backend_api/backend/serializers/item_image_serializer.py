from rest_framework import serializers
from ..models import ItemImage
from django.utils import timezone

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'unix_time', 'file_name', 'image', 'device_id']

    def create(self, validated_data):
        validated_data['unix_time'] = timezone.now().timestamp()
        return super().create(validated_data)