# coding: utf-8
from __future__ import unicode_literals, absolute_import

import six
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

from fias.fields import UUIDField
from fias.models.common import June2016Update
from fias.models.status import CenterSt, CurentSt, OperStat


__all__ = ['AddrObj']


@python_2_unicode_compatible
class AddrObj(June2016Update):
    """
    Классификатор адресообразующих элементов
    """
    class Meta:
        app_label = 'fias'
        verbose_name = 'Адресообразующий элемент'
        verbose_name_plural = 'Адресообразующие элементы'
        index_together = (
            ('aolevel', 'shortname'),
            ('shortname', 'formalname'),
        )
        ordering = ['aolevel', 'formalname']

    aoguid = UUIDField('Глобальный уникальный идентификатор адресного объекта', primary_key=True)
    parentguid = UUIDField('Идентификатор объекта родительского объекта', blank=True, null=True, db_index=True)
    aoid = UUIDField('Уникальный идентификатор записи', db_index=True, unique=True)
    previd = UUIDField('Идентификатор записи связывания с предыдушей исторической записью', blank=True, null=True)
    nextid = UUIDField('Идентификатор записи  связывания с последующей исторической записью', blank=True, null=True)

    formalname = models.CharField('Формализованное наименование', max_length=120, db_index=True)
    offname = models.CharField('Официальное наименование', max_length=120, blank=True, null=True)
    shortname = models.CharField('Краткое наименование типа объекта', max_length=10, db_index=True)
    aolevel = models.PositiveSmallIntegerField('Уровень адресного объекта', db_index=True)

    # KLADE
    regioncode = models.CharField('Код региона', max_length=2)
    autocode = models.CharField('Код автономии', max_length=1)
    areacode = models.CharField('Код района', max_length=3)
    citycode = models.CharField('Код города', max_length=3)
    ctarcode = models.CharField('Код внутригородского района', max_length=3)
    placecode = models.CharField('Код населенного пункта', max_length=3)
    plancode = models.CharField('Код элемента планировочной структуры', max_length=4)
    streetcode = models.CharField('Код улицы', max_length=4)
    extrcode = models.CharField('Код дополнительного адресообразующего элемента', max_length=4)
    sextcode = models.CharField('Код подчиненного дополнительного адресообразующего элемента', max_length=3)

    # KLADR
    code = models.CharField('Код адресного объекта одной строкой с признаком актуальности из КЛАДР 4.0',
                            max_length=17, blank=True, null=True)
    plaincode = models.CharField('Код адресного объекта из КЛАДР 4.0 одной строкой',
                                 help_text='Без признака актуальности (последних двух цифр)',
                                 max_length=15, blank=True, null=True)

    actstatus = models.BooleanField('Статус исторической записи в жизненном цикле адресного объекта', default=False)
    centstatus = models.ForeignKey(CenterSt, verbose_name='Статус центра', default=0)
    operstatus = models.ForeignKey(OperStat, verbose_name='Статус действия над записью – причина появления записи', default=0)
    currstatus = models.ForeignKey(CurentSt, verbose_name='Статус актуальности КЛАДР 4',
                                   help_text='последние две цифры в коде', default=0)

    livestatus = models.BooleanField('Признак действующего адресного объекта', default=False)

    def full_name(self, depth=None, formal=False):
        assert isinstance(depth, six.integer_types), 'Depth must be integer'

        if not self.parentguid or self.aolevel <= 1 or depth <= 0:
            if formal:
                return self.get_formal_name()
            return self.get_natural_name()
        else:
            parent = AddrObj.objects.get(pk=self.parentguid)
            return '{0}, {1}'.format(parent.full_name(depth-1, formal), self)

    def get_natural_name(self):
        if self.aolevel == 1:
            return '{0} {1}'.format(self.formalname, self.shortname)
        return self.get_formal_name()

    def get_formal_name(self):
        return '{0} {1}'.format(self.shortname, self.formalname)

    def __str__(self):
        return self.get_natural_name()

    def full_address(self):
        return self.full_name(5)
