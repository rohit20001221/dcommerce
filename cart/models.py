from django.db import models
from django.contrib.auth.models import User
from accounts.models import Farmer
import random
import uuid
# Create your models here.

def f():
    d = uuid.uuid4()
    str = d.hex
    return str[0:16]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"Cart({self.user.username})"


class CartItem(models.Model):
    item_id = models.IntegerField(null=True)
    name = models.CharField(max_length=60)
    price = models.FloatField()
    image = models.FileField(upload_to='user/items/')
    quantity = models.IntegerField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, related_name='items',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"item({self.cart}, {self.name})"

class Order(models.Model):
    item = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, default='')
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=1000, default="")
    received = models.BooleanField(default=False)
    e = models.CharField(max_length=18 , default = f)
    def __str__(self):
        return f"{self.pk}"
