# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from fias.fields import UUIDField

__all__ = ['Common', 'June2016Update']


class Common(models.Model):

    class Meta:
        abstract = True

    ifnsfl = models.PositiveIntegerField('Код ИФНС ФЗ', blank=True, null=True)
    terrifnsfl = models.PositiveIntegerField('Код территориального участка ИФНС ФЛ', blank=True, null=True)
    ifnsul = models.PositiveIntegerField('Код ИФНС ЮЛ', blank=True, null=True)
    terrifnsul = models.PositiveIntegerField('Код территориального участка ИФНС ЮЛ', blank=True, null=True)

    okato = models.BigIntegerField('ОКАТО', blank=True, null=True)
    oktmo = models.BigIntegerField('ОКТМО', blank=True, null=True)

    postalcode = models.PositiveIntegerField('Почтовый индекс', blank=True, null=True)

    updatedate = models.DateField('Дата время внесения записи')
    startdate = models.DateField('Начало действия записи')
    enddate = models.DateField('Окончание действия записи')
    normdoc = UUIDField('Внешний ключ на нормативный документ', blank=True, null=True)


class June2016Update(Common):

    class Meta:
        abstract = True

    cadnum = models.CharField('Кадастровый номер', max_length=100, blank=True, null=True)
    divtype = models.CharField('Тип адресации', max_length=1, default=0)
