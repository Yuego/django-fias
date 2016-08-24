# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField

__all__ = ['NormDoc', 'NDocType']


class NDocType(models.Model):
    """
    Состав и структура файла с информацией
    по типу нормативного документа в БД ФИАС
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Тип нормативного документа'
        verbose_name_plural = 'Типы нормативных документов'

    ndtypeid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор записи (ключ)')
    name = models.CharField('Наименование типа нормативного документа', max_length=250)


class NormDoc(models.Model):

    class Meta:
        app_label = 'fias'

    normdocid = UUIDField(primary_key=True)
    docname = models.TextField(blank=True, null=True)
    docdate = models.DateField(blank=True, null=True)
    docnum = models.CharField(max_length=20, blank=True, null=True)
    doctype = models.PositiveIntegerField()
    docimgid = models.PositiveIntegerField(blank=True, null=True)
