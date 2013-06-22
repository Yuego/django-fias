#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

__all__ = ['IFNS']


class IFNS(models.Model):

    class Meta:
        abstract = True

    ifnsfl = models.PositiveIntegerField(blank=True, null=True)
    terrifnsfl = models.PositiveIntegerField(blank=True, null=True)
    ifnsul = models.PositiveIntegerField(blank=True, null=True)
    terrifnsul = models.PositiveIntegerField(blank=True, null=True)

    okato = models.BigIntegerField(blank=True, null=True)
    oktmo = models.IntegerField(blank=True, null=True)

    updatedate = models.DateField()