from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=20)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.TextField()

    def __str__(self):
        return f'{self.user.username}({self.state})'

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.TextField()
    mid = models.CharField(max_length=100,default="iSSLla27754627519933")
    mkey = models.CharField(max_length=100,default="2tvvg2qwvazCh5tD")
    def __str__(self):
        return f"{self.name}({self.phonenumber})"
