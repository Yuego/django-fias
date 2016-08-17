# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.common import Common

__all__ = ['LandMark']


class LandMark(Common):

    class Meta:
        app_label = 'fias'

    landid = UUIDField()
    landguid = UUIDField(primary_key=True)
    aoguid = UUIDField()

    location = models.TextField()

    cadnum = models.CharField(max_length=100, blank=True, null=True)
