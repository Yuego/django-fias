#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.bulk import BulkCreate
from fias.models import AddrObj, LandMark
from .base import LoaderBase


class Loader(LoaderBase):

    def _init(self):
        self._model = LandMark
        self._bulk = BulkCreate(LandMark, 'landguid', 'updatedate')

    def process_row(self, row):
        if row.tag == 'Landmark':
            end_date = self._str_to_date(row.attrib['ENDDATE'])
            if end_date < self._today:
                print ('Out of date entry. Skipping...')
                return

            start_date = self._str_to_date(row.attrib['STARTDATE'])
            if start_date > self._today:
                print ('Date in future - skipping...')
                return

            related_attrs = dict()
            try:
                related_attrs['aoguid'] = AddrObj.objects.get(pk=row.attrib['AOGUID'])
            except AddrObj.DoesNotExist:
                print ('AddrObj with GUID `{0}` not found. Skipping house...'.format(row.attrib['AOGUID']))
                return

            self._bulk.push(row, related_attrs=related_attrs)
