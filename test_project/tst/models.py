from django.db import models

# Create your models here.

from fias.fields import AddressField
from fias.models import FIASAddress, FIASAddressWithArea

class Item(models.Model):
    
    title = models.CharField('title', max_length=100)

    location = AddressField()

class CachedAddress(FIASAddress):
    pass


class CachedAddressWithArea(FIASAddressWithArea):
    pass
