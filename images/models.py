from django.db import models

# Create your models here.
class Image(models.Model):
    tag = models.CharField(max_length=100)
    image = models.FileField(upload_to='images/')


    def __str__(self):
        return self.tag
