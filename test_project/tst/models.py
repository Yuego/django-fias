from django.db import models

# Create your models here.

from fias.fields import AddressField

class Item(models.Model):
    
    title = models.CharField('Title', max_length=100)

    location = AddressField()
