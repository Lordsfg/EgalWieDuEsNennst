from rest_framework import serializers

from ..models import ProductType


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
