#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from fias.fields import UUIDField
from fias.models.common import June2016Update
from fias.models.status import OperStat


__all__ = ['Stead']


@python_2_unicode_compatible
class Stead(June2016Update):
    """
    Сведения о земельных участках
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Земельный участок'
        verbose_name_plural = 'Земельные участки'

    steadguid = UUIDField('Глобальный уникальный идентификатор адресного объекта (земельного участка)',
                          primary_key=True)
    parentguid = UUIDField('Идентификатор объекта родительского объекта', blank=True, null=True, db_index=True)
    steadid = UUIDField('Уникальный идентификатор записи', unique=True)
    previd = UUIDField('Идентификатор записи связывания с предыдушей исторической записью', blank=True, null=True)
    nextid = UUIDField('Идентификатор записи  связывания с последующей исторической записью', blank=True, null=True)

    number = models.CharField('Номер земельного участка', max_length=120, blank=True, null=True)
    regioncode = models.CharField('Код региона', max_length=2)

    operstatus = models.ForeignKey(OperStat, verbose_name='Статус действия над записью – причина появления записи',
                                   default=0)
    livestatus = models.BooleanField('Признак действующего адресного объекта', default=False)

    def __str__(self):
        return self.number
