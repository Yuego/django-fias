#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fias.fields import UUIDField
from fias.models.common import June2016Update
from fias.models.status import OperStat


__all__ = ['Stead']


@python_2_unicode_compatible
class Stead(June2016Update):
    """
    Сведения о земельных участках
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Земельный участок'
        verbose_name_plural = 'Земельные участки'

    steadguid = UUIDField(primary_key=True)
    parentguid = UUIDField(blank=True, null=True, db_index=True)
    steadid = UUIDField(unique=True)
    previd = UUIDField(blank=True, null=True)
    nextid = UUIDField(blank=True, null=True)

    number = models.CharField(max_length=120, blank=True, null=True)
    regioncode = models.CharField(max_length=2)

    operstatus = models.ForeignKey(OperStat)
    livestatus = models.BooleanField(default=False)

    def __str__(self):
        return self.number
