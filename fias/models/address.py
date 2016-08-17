# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.text import force_text
from django.utils.translation import ugettext_lazy as _

from fias.models.addrobj import AddrObj
from fias.fields import AddressField, ChainedAreaField

__all__ = ['FIASAddress', 'FIASAddressWithArea',
           'FIASHouse',
           'FIASFullAddress', 'FIASFullAddressWithArea']


class FIASAddress(models.Model):

    class Meta:
        abstract = True

    address = AddressField(verbose_name=_('address'), related_name='+')

    full_address = models.CharField(_('full address'), max_length=255, blank=True, editable=False)
    short_address = models.CharField(_('street address'), max_length=255, blank=True, editable=False)

    def _update_address(self):
        full_addr = [force_text(self.address)]
        short_addr = []

        def make_addr(obj):
            if obj.aolevel > 3:
                short_addr.append(obj)

            if obj.aolevel > 1:
                try:
                    parent = AddrObj.objects.get(aoguid=obj.parentguid)
                except AddrObj.DoesNotExist:
                    return
                else:
                    full_addr.append(force_text(parent))
                    make_addr(parent)

        make_addr(self.address)

        self.full_address = ', '.join(full_addr[::-1])
        self.short_address = ', '.join(force_text(obj) for obj in short_addr[::-1] if obj.aolevel > 4)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.pk:
            old_obj = self._meta.concrete_model.objects.get(pk=self.pk)

            if self.address != old_obj.address:
                self._update_address()
        else:
            self._update_address()

        super(FIASAddress, self).save(force_insert, force_update, using, update_fields)


class FIASAddressWithArea(FIASAddress):

    class Meta:
        abstract = True

    area = ChainedAreaField(AddrObj, address_field='address', related_name='+')


class FIASHouse(models.Model):

    class Meta:
        abstract = True

    house = models.CharField(_('house number'), null=True, blank=True)
    corps = models.CharField(_('corps'), max_length=2, blank=True, default='')
    building = models.CharField(_('building'), null=True, blank=True)
    apartment = models.CharField(_('apartment'), null=True, blank=True)


class GetAddressMixin(object):

    def _get_full_address(self):
        addr = self.full_address

        if self.house:
            addr = '%s, %s' % (addr, self.house)
        if self.corps:
            addr += self.corps

        return addr

    def _get_short_address(self):
        addr = self.short_address if self.short_address else self.full_address

        if self.house:
            addr = '%s, %s' % (addr, self.house)
        if self.corps:
            addr += self.corps

        return addr


class FIASFullAddress(FIASAddress, FIASHouse, GetAddressMixin):

    class Meta:
        abstract = True


class FIASFullAddressWithArea(FIASAddressWithArea, FIASHouse, GetAddressMixin):

    class Meta:
        abstract = True
