from django.db import models

from .item_model import Item

class ItemImage(models.Model):
    # ID is the UNIX timestamp
    id = models.AutoField(primary_key=True)
    unix_time = models.BigIntegerField(null=True, blank=True, default=None)
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
