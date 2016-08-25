#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fias.fields import UUIDField
from fias.models.house import House
from fias.models.status import OperStat

__all__ = ['Room']


@python_2_unicode_compatible
class Room(models.Model):
    """
    Сведения о помещениях
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    houseguid = models.ForeignKey(House)
    roomguid = UUIDField(db_index=True, unique=True)
    roomid = UUIDField(primary_key=True)
    previd = UUIDField(blank=True, null=True)
    nextid = UUIDField(blank=True, null=True)
    flatnumber = models.CharField(max_length=50)
    flattype = models.IntegerField()
    roomnumber = models.CharField(max_length=50, blank=True, null=True)
    roomtype = models.IntegerField(blank=True, null=True)
    regioncode = models.CharField(max_length=2)
    postalcode = models.PositiveIntegerField(blank=True, null=True)
    updatedate = models.DateField()

    startdate = models.DateField()
    enddate = models.DateField()

    livestatus = models.BooleanField(default=False)

    normdoc = UUIDField(blank=True, null=True)

    operstatus = models.ForeignKey(OperStat, default=0)

    cadnum = models.CharField(max_length=100, blank=True, null=True)
    roomcadnum = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.flatnumber
