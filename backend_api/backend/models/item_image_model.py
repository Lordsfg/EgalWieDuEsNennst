from django.db import models

from .item_model import Item

class ItemImage(models.Model):
    id = models.BigIntegerField(primary_key=True)
    file_name = models.CharField(max_length=250)
    device_id = models.ForeignKey(
        Item,
        null= True,
        blank=True,
        on_delete=models.CASCADE,
        default=None
    )


    class Meta:
        db_table = 'ItemImages'
