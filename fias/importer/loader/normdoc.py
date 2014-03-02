#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.bulk import BulkCreate
from fias.models import NormDoc
from .base import LoaderBase


class Loader(LoaderBase):

    def _init(self):
        self._model = NormDoc
        self._bulk = BulkCreate(NormDoc, 'normdocid')

    def process_row(self, row):
        if row.tag == 'NormativeDocument':
            self._bulk.push(row)
