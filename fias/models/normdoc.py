#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField

__all__ = ['NormDoc']


class NormDoc(models.Model):

    class Meta:
        app_label = 'fias'

    normdocid = UUIDField(primary_key=True)
    docname = models.TextField(blank=True)
    docdate = models.DateField(blank=True, null=True)
    docnum = models.CharField(max_length=20, blank=True, null=True)
    doctype = models.PositiveIntegerField()
    docimgid = models.PositiveIntegerField(blank=True, null=True)
