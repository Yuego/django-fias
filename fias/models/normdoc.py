# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fias.fields import UUIDField

__all__ = ['NormDoc', 'NDocType']


@python_2_unicode_compatible
class NDocType(models.Model):
    """
    Тип нормативного документа
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Тип нормативного документа'
        verbose_name_plural = 'Типы нормативных документов'

    ndtypeid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор записи (ключ)')
    name = models.CharField('Наименование типа нормативного документа', max_length=250)

    def __str__(self):
        return self.name


class NormDoc(models.Model):
    """
    Сведения по нормативному документу,
    являющемуся основанием присвоения адресному элементу наименования
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Нормативный документ'
        verbose_name_plural = 'Нормативные документы'

    normdocid = UUIDField(primary_key=True, verbose_name='Идентификатор нормативного документа')
    docname = models.TextField('Наименование документа', blank=True, null=True)
    docdate = models.DateField('Дата документа', blank=True, null=True)
    docnum = models.CharField('Номер документа', max_length=20, blank=True, null=True)
    doctype = models.ForeignKey(NDocType, verbose_name='Тип документа', default=0)
    docimgid = models.PositiveIntegerField('Идентификатор образа (внешний ключ)', blank=True, null=True)
