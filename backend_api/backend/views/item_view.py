from .base_view import BaseCRUDAPIView
from ..serializers import ItemSerializer, ItemReturnModel
from ..models import Item
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

class ItemView(BaseCRUDAPIView):
    queryset = Item.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    lookup_fields = {'id': 'id'}

    @api_view(['GET'])
    def get_borrowed_items_by_user_id(request, user_id: int):
        
        borrowed_items = Item.objects.filter(borrowed_by_user__id=user_id)

        serializer = ItemSerializer(borrowed_items, many=True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def get_item_details(request, item_id: int):
        item = Item.objects.get(id=item_id)
        serializer = ItemReturnModel(item)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def get_all_items(request):
        items = Item.objects.all()
        serializer = ItemReturnModel(items, many=True)
        return Response(serializer.data)

