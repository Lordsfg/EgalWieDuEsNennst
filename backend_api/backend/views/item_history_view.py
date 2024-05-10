from .base_view import BaseCRUDAPIView
from ..serializers import ItemHistorySerializer
from ..models import ItemHistory
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Item

class ItemHistoryView(BaseCRUDAPIView):
    queryset = ItemHistory.objects.all()
    serializer_class = ItemHistorySerializer
    lookup_fields = {'id': 'id', 'item': 'item', 'user': 'user', 'item_history_type': 'item_history_type', 'room': 'room', 'date': 'date'}
    # Override the post method
    def post(self, request, *args, **kwargs):
        # Extract user_id and item_id from POST request data
        user_id = request.data.get('user')
        item_id = request.data.get('item')

        # 1 = borrow, 2 = return
        history_type_id = request.data.get('item_history_type')

        location_id = request.data.get('room')

        # Check if both user_id and item_id are provided
        if user_id is None or item_id is None or history_type_id is None:
            return Response({'error': 'Both user_id and item_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Item object
        item = get_object_or_404(Item, pk=item_id)

        # Patch Item table to update borrowed_by_user_id column
        if history_type_id == 1:
            item.borrowed_by_user_id = user_id
        if history_type_id == 2:
            item.borrowed_by_user_id = None
            item.current_room_id = location_id


        item.save()

        ### Save history
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Item and ItemHistory updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetItemHistoryByItemId(BaseCRUDAPIView):
    queryset = ItemHistory.objects.all()
    serializer_class = ItemHistorySerializer
    def get(self, request, id):
        item_history = ItemHistory.objects.filter(item__id=id)
        serializer = ItemHistorySerializer(item_history, many=True)
        return Response(serializer.data)