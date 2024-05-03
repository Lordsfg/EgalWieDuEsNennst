from .base_view import BaseCRUDAPIView
from ..serializers import ItemSerializer, ItemReturnModel
from ..models import Item, User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests


class ItemView(BaseCRUDAPIView):
    queryset = Item.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    lookup_fields = {'id': 'id'}

    @api_view(['GET'])
    def get_borrowed_items_by_user_id(request, user_id: int):
        
        borrowed_items = Item.objects.filter(borrowed_by_user__id=user_id)

        # serializer = ItemSerializer(borrowed_items, many=True)
        serializer = ItemReturnModel(borrowed_items, many=True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def get_item_details(request, item_id: int):
        item = Item.objects.get(id=item_id)
        serializer = ItemReturnModel(item)
        return Response(serializer.data)
    @api_view(['GET'])
    def get_all_items(request):
        items = Item.objects.all().order_by('-id')
        serializer = ItemReturnModel(items, many=True)
        return Response(serializer.data)

    @api_view(['POST'])
    def add_new_items(request):
        items = request.data
        base_url = "http://localhost:8000/api/v1/"
        for item in items:
            
            fields = item
            
            if "product_type" not in fields:
                return Response({"error": "Product type is required"}, status=400)
            
            product_type_data = fields.pop("product_type")
            room_data = fields.pop("current_room")

            # Update product_type, create new type if id not exists
            if "id" in product_type_data and product_type_data["id"] is not None:
                product_type_id = product_type_data["id"]
            else:
                # Create new product type
                product_type_response = requests.post(f"{base_url}product-type/", json=product_type_data)
                if product_type_response.status_code > 299:
                    print(f"ERROR creating product type: {product_type_response.content}")
                    continue
                else:
                    product_type_id = product_type_response.json()["id"]
            
            fields["product_type"] = product_type_id

            ## update room, create new room if id not exists
            if "id" in room_data and room_data["id"] is not None:
                room_id = room_data["id"]
            else:
                room_response = requests.post(f"{base_url}room/", json=room_data)
                if room_response.status_code > 299:
                    print(f'error creating room: {room_response.content}')
                else:
                    room_id = room_response.json()["id"]
            fields["current_room"] = room_id

            
            response = requests.post(f"{base_url}item/", json=fields)
            if response.status_code > 299:
                print(f"ERROR: model: Item, response: {response.content}")
                return Response({"error": f"Failed to add item: {fields}"}, status=500)  # Return an error response

        return Response({"message": f"Successfully added item '{product_type_data['name']}'."}, status=201)