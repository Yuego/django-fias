#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from fias.fields import UUIDField

__all__ = ['Common']


class Common(models.Model):

    class Meta:
        abstract = True

    ifnsfl = models.PositiveIntegerField(blank=True, null=True)
    terrifnsfl = models.PositiveIntegerField(blank=True, null=True)
    ifnsul = models.PositiveIntegerField(blank=True, null=True)
    terrifnsul = models.PositiveIntegerField(blank=True, null=True)

    okato = models.BigIntegerField(blank=True, null=True)
    oktmo = models.BigIntegerField(blank=True, null=True)

    postalcode = models.PositiveIntegerField(blank=True, null=True)

    updatedate = models.DateField()
    startdate = models.DateField()
    enddate = models.DateField()
    normdoc = UUIDField(blank=True, null=True, auto=False)
