from django.db import models

from .product_type_model import ProductType
from .room_model import Room
from .user_model import User


class Item(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    product_type = models.ForeignKey(
        ProductType,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    current_room = models.ForeignKey(
        Room,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    annotation = models.TextField(
        max_length=10000,
        null=True,
        blank=True
    )

    borrowed_by_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    qr_code = models.TextField(
        max_length=10000,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Item'
