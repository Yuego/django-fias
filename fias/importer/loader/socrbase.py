#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.bulk import BulkCreate
from fias.models import SocrBase
from .base import LoaderBase


class Loader(LoaderBase):

    def _init(self):
        self._model = SocrBase
        self._bulk = BulkCreate(SocrBase, 'kod_t_st')

    def process_row(self, row):
        if row.tag == 'AddressObjectType':
            self._bulk.push(row)
