from rest_framework import serializers

from ..models import ItemHistoryType


class ItemHistoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemHistoryType
        fields = ['id', 'name']
        read_only_fields = ['id']
