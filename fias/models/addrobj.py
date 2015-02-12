#coding: utf-8
from __future__ import unicode_literals, absolute_import

import six
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models

from fias.config import FIAS_DATABASE_ALIAS
from fias.fields import UUIDField
from fias.models.common import Common


__all__ = ['AddrObj']

@python_2_unicode_compatible
class AddrObj(Common):

    class Meta:
        app_label = 'fias'
        index_together = (
            ('aolevel', 'shortname'),
            ('shortname', 'formalname'),
        )
        ordering = ['aolevel', 'formalname']

    aoguid = UUIDField(primary_key=True)
    parentguid = UUIDField(blank=True, null=True, auto=False, db_index=True)
    aoid = UUIDField(db_index=True, unique=True)
    previd = UUIDField(blank=True, null=True, auto=False)
    nextid = UUIDField(blank=True, null=True, auto=False)

    formalname = models.CharField(max_length=120, db_index=True)
    offname = models.CharField(max_length=120, blank=True, null=True)
    shortname = models.CharField(max_length=10, db_index=True)
    aolevel = models.PositiveSmallIntegerField(db_index=True)

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

    actstatus = models.BooleanField(default=False)
    centstatus = models.PositiveSmallIntegerField()
    operstatus = models.PositiveSmallIntegerField()
    currstatus = models.PositiveSmallIntegerField()

    livestatus = models.BooleanField(default=False)

    def full_name(self, depth=None, formal=False):
        assert isinstance(depth, six.integer_types), 'Depth must be integer'

        if not self.parentguid or self.aolevel <= 1 or depth <= 0:
            if formal:
               return self.get_formal_name()
            return self.get_natural_name()
        else:
            parent = AddrObj.objects.get(pk=self.parentguid)
            return '{0}, {1}'.format(parent.full_name(depth-1, formal), self)

    def get_natural_name(self):
        if self.aolevel == 1:
            return '{0} {1}'.format(self.formalname, self.shortname)
        return self.get_formal_name()

    def get_formal_name(self):
        return '{0} {1}'.format(self.shortname, self.formalname)

    def __str__(self):
        return self.get_natural_name()

    def full_address(self):
        return self.full_name(5)
