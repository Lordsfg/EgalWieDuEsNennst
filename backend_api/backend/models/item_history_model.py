from django.db import models

from .item_model import Item
from .user_model import User
from .item_history_type_model import ItemHistoryType
from .room_model import Room


class ItemHistory(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    item = models.ForeignKey(
        Item,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    item_history_type = models.ForeignKey(
        ItemHistoryType,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'ItemHistory'
