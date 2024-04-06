from django.urls import path
from . import views
from .views import ItemImageView
from django.conf import settings
from django.conf.urls.static import static

api_pattern = "api/v1/"

urlpatterns = [
  # User
  path(f'{api_pattern}user/', views.UserView.as_view(), name='user-list'),
  path(f'{api_pattern}user/<str:lookup_field>/<str:lookup_value>/', views.UserView.as_view(), name='user-lookup'),

  # UserType
  path(f'{api_pattern}user-type/', views.UserTypeView.as_view(), name='user-type-list'),
  path(f'{api_pattern}user-type/<str:lookup_field>/<str:lookup_value>/', views.UserTypeView.as_view(), name='user-type-lookup'),

  # Room
  path(f'{api_pattern}room/', views.RoomView.as_view(), name='room-list'),
  path(f'{api_pattern}room/<str:lookup_field>/<str:lookup_value>/', views.RoomView.as_view(), name='room-lookup'),

  # ProductType
  path(f'{api_pattern}product-type/', views.ProductTypeView.as_view(), name='product-type-list'),
  path(f'{api_pattern}product-type/<str:lookup_field>/<str:lookup_value>/', views.ProductTypeView.as_view(), name='product-type-lookup'),

  # Item
  path(f'{api_pattern}item/', views.ItemView.as_view(), name='item-list'),
  path(f'{api_pattern}item/<str:lookup_field>/<str:lookup_value>/', views.ItemView.as_view(), name='item-lookup'),

  # Get all Items
  path(f'{api_pattern}items-all/', views.ItemView.get_all_items, name='item-return'),
  # Get item details by ID
  path(f'{api_pattern}item-details/<int:item_id>/', views.ItemView.get_item_details, name='item-details'),

  path(f'{api_pattern}items-new/', views.ItemView.add_new_items, name='item-new'),

  # ItemHistory
  path(f'{api_pattern}item-history/', views.ItemHistoryView.as_view(), name='item-history-list'),
  path(f'{api_pattern}item-history/<str:lookup_field>/<str:lookup_value>/', views.ItemHistoryView.as_view(), name='item-history-lookup'),

  # ItemHistoryType
  path(f'{api_pattern}item-history-type/', views.ItemHistoryTypeView.as_view(), name='item-history-type-list'),
  path(f'{api_pattern}item-history-type/<str:lookup_field>/<str:lookup_value>/', views.ItemHistoryTypeView.as_view(), name='item-history-type-lookup'),

  # BorrowedItems
  path(f'{api_pattern}borrowed_items_by_user/<int:user_id>/', views.ItemView.get_borrowed_items_by_user_id, name='get_borrowed_items'),

  path(f'{api_pattern}items/<int:id>/image/', ItemImageView.as_view(), name='item-image-detail'),
]

# Retrieve image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
