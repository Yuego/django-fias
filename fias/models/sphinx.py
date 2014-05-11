#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField


class AddrObjIndex(models.Model):

    class Meta:
        app_label = 'fias'

    aoguid = UUIDField()
    aolevel = models.PositiveSmallIntegerField()
    scname = models.TextField()
    fullname = models.TextField()
    item_weight = models.PositiveSmallIntegerField(default=64)
