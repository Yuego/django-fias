#coding: utf-8
from __future__ import unicode_literals, absolute_import

import six

from django.db import models

from fias.fields import UUIDField
from fias.models.ifns import IFNS
from fias.models.normdoc import NormDoc

__all__ = ['AddrObj']


class AddrObjBase(IFNS):

    class Meta:
        abstract = True
        index_together = (
            ('aolevel', 'shortname'),
            ('shortname', 'formalname'),
        )
        ordering = ['aolevel', 'formalname']

    aoguid = UUIDField(primary_key=True)
    parentguid = UUIDField(blank=True, null=True, db_index=True)
    aoid = UUIDField(db_index=True, unique=True)
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

    normdoc = UUIDField(blank=True, null=True)
    livestatus = models.BooleanField()

    def full_name(self, depth=None):
        assert isinstance(depth, six.integer_types), 'Depth must be integer'

        if not self.parentguid or self.aolevel <= 1 or depth <= 0:
            return self.__unicode__()
        else:
            parent = AddrObj.objects.get(pk=self.parentguid)
            return '{}, {}'.format(parent.full_name(depth-1), self)

    def __unicode__(self):
        return '{} {}'.format(self.shortname, self.formalname)


class AddrObj(AddrObjBase):

    class Meta:
        app_label = 'fias'