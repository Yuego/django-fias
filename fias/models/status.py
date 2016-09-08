#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

__all__ = [
    'ActStat', 'CenterSt', 'CurentSt',
    'EstStat', 'HSTStat', 'IntvStat',
    'OperStat', 'StrStat'
]


@python_2_unicode_compatible
class ActStat(models.Model):
    """
    Статус актуальности ФИАС
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус актуальности ФИАС'
        verbose_name_plural = 'Статусы актуальности ФИАС'

    actstatid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор статуса (ключ)')
    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CenterSt(models.Model):
    """
    Статус центра
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус центра'
        verbose_name_plural = 'Статусы центров'

    centerstid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор статуса')
    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CurentSt(models.Model):
    """
    Статус актуальности КЛАДР 4.0
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус актуальности КЛАДР 4.0'
        verbose_name_plural = 'Статусы актуальности КЛАДР 4.0'

    curentstid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор статуса (ключ)')
    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EstStat(models.Model):
    """
    Признак владения
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Признак владения'
        verbose_name_plural = 'Признаки владения'

    eststatid = models.PositiveIntegerField(primary_key=True, verbose_name='Признак владения')
    name = models.CharField('Наименование', max_length=20)
    shortname = models.CharField('Краткое наименование', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class HSTStat(models.Model):
    """
    Статус состояния домов
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус состояния домов'
        verbose_name_plural = 'Статусы состояния домов'

    housestid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор статуса')
    name = models.CharField('Наименование', max_length=60)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class IntvStat(models.Model):
    """
    Статус интервалов домов
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус интервала домов'
        verbose_name_plural = 'Статусы интервалов домов'

    intvstatid = models.PositiveIntegerField(primary_key=True,
                                             verbose_name='Идентификатор статуса (обычный, четный, нечетный)')
    name = models.CharField('Наименование', max_length=60)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OperStat(models.Model):
    """
    Статус действия
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Статус действия'
        verbose_name_plural = 'Статусы действия'

    operstatid = models.PositiveIntegerField(primary_key=True, verbose_name='Идентификатор статуса (ключ)')
    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StrStat(models.Model):
    """
    Признак строения
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Признак строения'
        verbose_name_plural = 'Признаки строения'

    strstatid = models.PositiveIntegerField('Признак строения', primary_key=True)
    name = models.CharField('Наименование', max_length=20)
    shortname = models.CharField('Краткое наименование', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
