from django.db import models
from accounts.models import Farmer
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField()
    image = models.FileField(upload_to='items/')
    quantity = models.IntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} {self.price}"
