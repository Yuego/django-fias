#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.text import force_unicode
from django.utils.translation import ugettext_lazy as _

from fias.models.addrobj import AddrObj
from fias.fields import AddressField

__all__ = ['FIASAddress', 'FIASHouse', 'FIASFullAddress']


class FIASAddress(models.Model):

    _LEVELS = {
        1: 'region',
        2: 'auto',
        3: 'area',
        4: 'city',
        5: 'ctar',
        6: 'place',
        7: 'street',
        90: 'ext',
        91: 'sext',
    }

    class Meta:
        abstract = True

    address = AddressField(AddrObj, verbose_name=_('address'))

    full_address = models.CharField(_('full address'), max_length=255, blank=True, editable=False)
    short_address = models.CharField(_('short address'), max_length=255, blank=True, editable=False)

    def _update_address(self):
        full_addr = [force_unicode(self.address)]
        short_addr = []

        def make_addr(obj):
            if obj.aolevel > 3:
                short_addr.append(force_unicode(obj))

            level = int(obj.aolevel)
            attr = self._LEVELS[level]
            if hasattr(self, attr):
                setattr(self, attr, obj)

            if obj.aolevel > 1:
                try:
                    parent = AddrObj.objects.get(aoguid=obj.parentguid)
                except AddrObj.DoesNotExist:
                    return
                else:
                    full_addr.append(force_unicode(parent))
                    make_addr(parent)

        make_addr(self.address)

        self.full_address = ', '.join(full_addr[::-1])
        self.short_address = ', '.join(short_addr[::-1])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.pk:
            old_obj = self._meta.concrete_model.objects.get(pk=self.pk)

            if self.address != old_obj.address:
                self._update_address()
        else:
            self._update_address()

        super(FIASAddress, self).save(force_insert, force_update, using, update_fields)


class FIASHouse(models.Model):

    class Meta:
        abstract = True

    house = models.PositiveSmallIntegerField(_('house number'), max_length=3, null=True, blank=True)
    corps = models.CharField(_('corps'), max_length=2, blank=True, default='')
    apartment = models.PositiveSmallIntegerField(_('apartment'), max_length=3, null=True, blank=True)


class FIASFullAddress(FIASAddress, FIASHouse):

    class Meta:
        abstract = True
