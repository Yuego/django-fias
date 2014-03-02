#coding: utf-8
from __future__ import unicode_literals, absolute_import


from fias.importer.bulk import BulkCreate
from fias.importer.log import log
from fias.models import AddrObj
from .base import LoaderBase


class Loader(LoaderBase):

    def _init(self):
        self._model = AddrObj
        self._bulk = BulkCreate(AddrObj, 'aoguid', 'updatedate')

    def process_row(self, row):
        if row.tag == 'Object':
            # Пропускаем изменённые объекты
            if 'NEXTID' in row.attrib and row.attrib['NEXTID']:
                return
    
            start_date = self._str_to_date(row.attrib['STARTDATE'])
            if start_date > self._today:
                log.debug('Date in future - skipping...')
                return

            self._bulk.push(row)
