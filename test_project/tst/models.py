from django.db import models

# Create your models here.

from fias.fields import AddressField
from fias.models import FIASAddress, FIASAddressWithArea, FIASHouse

class Item(models.Model):
    
    title = models.CharField('title', max_length=100)

    location = AddressField()

#class CachedAddress(FIASAddress):
#    pass


#class CachedAddressWithArea(FIASAddressWithArea):
#    pass


#class CachedAddressWithHouse(FIASAddress, FIASHouse):
#    pass

#class NullableAddressItem(models.Model):
#    title = models.CharField('title', max_length=100)
#
#    location = AddressField(blank=True, null=True)
