# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models

from fias.fields import UUIDField
from fias.models.addrobj import AddrObj
from fias.models.common import Common, June2016Update
from fias.models.status import EstStat, IntvStat, StrStat

__all__ = ['House', 'HouseInt']


class House(June2016Update):
    """
    Сведения по номерам домов улиц городов и населенных пунктов
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Номер дома'
        verbose_name_plural = 'Номера домов'

    aoguid = models.ForeignKey(AddrObj, verbose_name='Идентификатор записи родительского объекта',
                               help_text='(улица, город, населенный пункт и т.п.)')
    houseguid = UUIDField('Глобальный уникальный идентификатор дома', primary_key=True)
    houseid = UUIDField('Уникальный идентификатор записи дома', unique=True)

    housenum = models.CharField('Номер дома', max_length=20, blank=True, null=True)
    eststatus = models.ForeignKey(EstStat, verbose_name='Признак владения', default=0)
    buildnum = models.CharField('Номер корпуса', max_length=10, blank=True, null=True)
    strucnum = models.CharField('Номер строения', max_length=10, blank=True, null=True)
    strstatus = models.ForeignKey(StrStat, verbose_name='Признак строения', default=0)

    statstatus = models.PositiveSmallIntegerField('Состояние дома')

    regioncode = models.CharField('Код региона', max_length=2, blank=True, null=True)

    counter = models.IntegerField('Счетчик записей домов для КЛАДР 4')


class HouseInt(Common):
    """
    Интервалы домов
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Интервал домов'
        verbose_name_plural = 'Интервалы домов'

    houseintid = UUIDField('Идентификатор записи интервала домов')
    intguid = UUIDField('Глобальный уникальный идентификатор интервала домов', primary_key=True)
    aoguid = models.ForeignKey(AddrObj, verbose_name='Идентификатор объекта родительского объекта',
                               help_text='(улица, город, населенный пункт и т.п.)')

    intstart = models.PositiveIntegerField('Значение начала интервала')
    intend = models.PositiveIntegerField('Значение окончания интервала')

    intstatus = models.ForeignKey(IntvStat, verbose_name='Статус интервала', default=0)

    counter = models.PositiveIntegerField('Счетчик записей домов для КЛАДР 4')
