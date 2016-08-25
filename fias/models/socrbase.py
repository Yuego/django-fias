# coding: utf-8
from __future__ import unicode_literals, absolute_import
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = ['SocrBase']


@python_2_unicode_compatible
class SocrBase(models.Model):
    """
    Тип адресного объекта
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Тип адресного объекта'
        verbose_name_plural = 'Типы адресных объектов'
        index_together = (
            ('level', 'scname'),
        )
        ordering = ['level', 'scname']

    level = models.PositiveSmallIntegerField('Уровень адресного объекта')
    scname = models.CharField('Краткое наименование типа объекта', max_length=10, default=" ")
    socrname = models.CharField('Полное наименование типа объекта', max_length=50, default=" ")
    kod_t_st = models.PositiveIntegerField('Ключевое поле', primary_key=True)

    item_weight = models.PositiveSmallIntegerField('Вес типа объекта', default=64,
                                                   help_text='Используется для сортировки результатов поиска'
                                                             ' с помощью Sphinx. Допустимые значения 1-128.'
                                                             ' Чем больше число, тем выше объекты данного'
                                                             ' типа в поиске.')

    def __str__(self):
        return self.socrname
