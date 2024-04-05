from .base_view import BaseCRUDAPIView
from ..serializers import ItemSerializer, ItemReturnModel, ItemImageSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models import ItemImage, Item
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

class ItemImageView(BaseCRUDAPIView):
    serializer_class = ItemImageSerializer
    queryset = ItemImage.objects.all()
    def get(self, request, pk):
        try:
            item_images = ItemImage.objects.filter(device_id=pk)
            serializer = ItemImageSerializer(item_images, many=True)
            return Response(serializer.data)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, pk):
        # Retrieve the Item instance based on the provided primary key
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Associate the Item instance with the ItemImage instance being created
        request.data['device_id'] = pk

        # Serialize and save the ItemImage instance
        serializer = ItemImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk):
        try:
            item_image = ItemImage.objects.get(pk=pk)
            serializer = ItemImageSerializer(item_image, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            item_image = ItemImage.objects.get(pk=pk)
            item_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)