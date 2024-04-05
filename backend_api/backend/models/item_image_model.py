from django.db import models

from .item_model import Item

class ItemImage(models.Model):
    # ID is the UNIX timestamp
    id = models.BigIntegerField(primary_key=True)
    file_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True, default=None)
    device_id = models.ForeignKey(
        Item,
        null= True,
        blank=True,
        on_delete=models.CASCADE,
        default=None
    )
    class Meta:
        db_table = 'ItemImages'
