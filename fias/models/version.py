#coding: utf-8
from __future__ import unicode_literals, absolute_import
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

__all__ = ['Version', 'Status']

@python_2_unicode_compatible
class Version(models.Model):

    class Meta:
        app_label = 'fias'

    ver = models.IntegerField(primary_key=True)
    date = models.DateField(db_index=True, blank=True, null=True)
    dumpdate = models.DateField(db_index=True)

    complete_xml_url = models.CharField(max_length=255)
    delta_xml_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{0} from {1}'.format(self.ver, self.dumpdate)


@python_2_unicode_compatible
class Status(models.Model):

    class Meta:
        app_label = 'fias'

    table = models.CharField(primary_key=True, max_length=15)
    ver = models.ForeignKey(Version)

    def __str__(self):
        return self.table
