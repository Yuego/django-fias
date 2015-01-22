#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.common import Common
from fias.models.addrobj import AddrObj

__all__ = ['House', 'HouseInt']


class House(Common):

    class Meta:
        app_label = 'fias'

    aoguid = models.ForeignKey(AddrObj)

    housenum = models.CharField(max_length=20, blank=True, null=True)
    eststatus = models.BooleanField(default=False)
    buildnum = models.CharField(max_length=10, blank=True, null=True)
    strucnum = models.CharField(max_length=10, blank=True, null=True)
    strstatus = models.PositiveSmallIntegerField()
    houseguid = UUIDField(primary_key=True)
    houseid = UUIDField()

    statstatus = models.PositiveSmallIntegerField()

    counter = models.IntegerField()


class HouseInt(Common):

    class Meta:
        app_label = 'fias'

    houseintid = UUIDField()
    intguid = UUIDField(primary_key=True)
    aoguid = models.ForeignKey(AddrObj)

    intstart = models.PositiveIntegerField()
    intend = models.PositiveIntegerField()

    intstatus = models.PositiveIntegerField()

    counter = models.PositiveIntegerField()

