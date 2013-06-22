#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from django_fias.fields import UUIDField
from django_fias.models.ifns import IFNS
from django_fias.models.normdoc import NormDoc

__all__ = ['AddrObj', 'AddrObjFuture']


class AddrObjBase(IFNS):

    class Meta:
        abstract = True
        index_together = (
            ('aolevel', 'shortname'),
            ('shortname', 'formalname'),
        )
        ordering = ['aolevel', 'formalname']

    aoguid = UUIDField(db_index=True, unique=True)
    parentguid = UUIDField(blank=True, null=True, db_index=True)
    aoid = UUIDField(primary_key=True)
    previd = UUIDField(blank=True, null=True)
    nextid = UUIDField(blank=True, null=True)

    startdate = models.DateField()
    enddate = models.DateField()

    formalname = models.CharField(max_length=120, db_index=True)
    offname = models.CharField(max_length=120, blank=True, null=True)
    shortname = models.CharField(max_length=10, db_index=True)
    aolevel = models.PositiveSmallIntegerField(db_index=True)
    postalcode = models.PositiveIntegerField(blank=True, null=True)

    #KLADE
    regioncode = models.CharField(max_length=2)
    autocode = models.CharField(max_length=1)
    areacode = models.CharField(max_length=3)
    citycode = models.CharField(max_length=3)
    ctarcode = models.CharField(max_length=3)
    placecode = models.CharField(max_length=3)
    streetcode = models.CharField(max_length=4)
    extrcode = models.CharField(max_length=4)
    sextcode = models.CharField(max_length=3)

    #KLADR
    code = models.CharField(max_length=17, blank=True, null=True)
    plaincode = models.CharField(max_length=15, blank=True, null=True)

    actstatus = models.BooleanField()
    centstatus = models.PositiveSmallIntegerField()
    operstatus = models.PositiveSmallIntegerField()
    currstatus = models.PositiveSmallIntegerField()

    normdoc = models.ForeignKey(NormDoc, blank=True, null=True)
    livestatus = models.BooleanField()

    def __unicode__(self):
        return '{} {}'.format(self.shortname, self.formalname)


class AddrObjFuture(AddrObjBase):

    class Meta:
        app_label = 'django_fias'


class AddrObj(AddrObjBase):

    class Meta:
        app_label = 'django_fias'