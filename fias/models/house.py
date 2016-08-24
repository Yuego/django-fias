# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.common import Common, June2016Update
from fias.models.status import EstStat, IntvStat, StrStat

__all__ = ['House', 'HouseInt']


class House(June2016Update):

    class Meta:
        app_label = 'fias'

    aoguid = UUIDField()

    housenum = models.CharField(max_length=20, blank=True, null=True)
    eststatus = models.ForeignKey(EstStat)
    buildnum = models.CharField(max_length=10, blank=True, null=True)
    strucnum = models.CharField(max_length=10, blank=True, null=True)
    strstatus = models.ForeignKey(StrStat)
    houseguid = UUIDField(primary_key=True)
    houseid = UUIDField()

    statstatus = models.PositiveSmallIntegerField()

    regioncode = models.CharField(max_length=2, blank=True, null=True)

    counter = models.IntegerField()


class HouseInt(Common):

    class Meta:
        app_label = 'fias'

    houseintid = UUIDField()
    intguid = UUIDField(primary_key=True)
    aoguid = UUIDField()

    intstart = models.PositiveIntegerField()
    intend = models.PositiveIntegerField()

    intstatus = models.ForeignKey(IntvStat)

    counter = models.PositiveIntegerField()

