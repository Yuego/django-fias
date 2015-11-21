#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import models
from fias.fields import UUIDField
from fias.models import (
    AddrObj,
    House, HouseInt,
    LandMark,
    NormDoc,
    SocrBase,
)


table_names = {
    'addrobj': AddrObj,
    'house': House,
    'houseint': HouseInt,
    'landmark': LandMark,
    'normdoc': NormDoc,
    'socrbase': SocrBase,
}


class ParentLookupException(Exception):
    pass


class TableIterator(object):

    def __init__(self, fd, model):
        self._fd = fd
        self.model = model

        self.related_fields = dict({
            (f.name, f) for f in self.model._meta.get_fields()
            if f.one_to_one or f.many_to_one
        })
        self.uuid_fields = dict({
            (f.name, f) for f in self.model._meta.get_fields()
            if isinstance(f, UUIDField)
        })
        self.date_fields = dict({
            (f.name, f) for f in self.model._meta.get_fields()
            if isinstance(f, models.DateField)
        })

    def __iter__(self):
        if self.model is None:
            return []

        return self

    def get_context(self):
        raise NotImplementedError()

    def get_next(self):
        raise NotImplementedError()

    def format_row(self, row):
        raise NotImplementedError()

    def process_row(self, row):
        try:
            row = dict(self.format_row(row))
        except ParentLookupException as e:
            return None

        return self.model(**row)

    def __next__(self):
        return self.get_next()

    next = __next__


class Table(object):
    name = None
    iterator = TableIterator

    def __init__(self, filename, **kwargs):
        self.filename = filename

        self.name = kwargs['name'].lower()
        self.model = table_names.get(self.name, None)

    def open(self, archive):
        return archive.open(self.filename)

    def rows(self, archive):
        raise NotImplementedError()
