#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.common import Common
from fias.models.addrobj import AddrObj

__all__ = ['LandMark']


class LandMark(Common):

    class Meta:
        app_label = 'fias'

    landid = UUIDField()
    landguid = UUIDField(primary_key=True)
    aoguid = models.ForeignKey(AddrObj)

    location = models.TextField()
