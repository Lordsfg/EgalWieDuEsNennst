from .base_view import BaseCRUDAPIView
from ..serializers import ItemSerializer, ItemReturnModel, ItemImageSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models import ItemImage, Item
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import os

class ItemImageView(BaseCRUDAPIView):
    serializer_class = ItemImageSerializer
    queryset = ItemImage.objects.all()
    def get(self, request, id):
        try:
            item_images = ItemImage.objects.filter(device_id=id)
            serializer = ItemImageSerializer(item_images, many=True)
            return Response(serializer.data)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Associate the Item instance with the ItemImage instance being created
        request.data['device_id'] = id

        # Serialize and save the ItemImage instance
        serializer = ItemImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, id):
        try:
            item_image = ItemImage.objects.get(pk=id)
            serializer = ItemImageSerializer(item_image, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            # all images of one item
            item_images = ItemImage.objects.filter(device_id=id)
            
            # Delete all images of one item
            for item_image in item_images:
                # Delete the associated image file from the media directory
                if item_image.image:
                    image_path = item_image.image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                # Delete the database record
                item_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ItemImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)