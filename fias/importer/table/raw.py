#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .table import Table, table_names


class RawModel(object):
    _db_model = None
    _dict = None

    def __init__(self, **kwargs):
        pk = self._db_model._meta.pk.name
        self._dict = kwargs

        for key, value in self._dict.items():
            setattr(self, key, value)

        setattr(self, 'pk', getattr(self, pk))

    def __getitem__(self, item):
        return self._dict[item]


def raw_model_factory(model):
    name = model.__name__ + 'Raw'
    return type(name, [RawModel], {'_db_model': model})


class RawTable(Table):

    def __init__(self, filename, **kwargs):
        self.filename = filename

        self.name = kwargs['name'].lower()
        model = table_names.get(self.name)
        self.model = raw_model_factory(model)

    def truncate(self):
        self._truncate(self.model._db_model)
