#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .table import Table, TableIterator
from .raw import RawTable

from dbfread import DBF, FieldParser


class ModelFieldParser(FieldParser):

    def parseC(self, field, data):
        result = super(ModelFieldParser, self).parseC(field, data)

        if not result:
            return None

        return result


class DBFTable(Table):

    def rows(self, tablelist):
        db = DBF(
            self.open(tablelist=tablelist),
            lowernames=True,
            parserclass=ModelFieldParser,
            recfactory=lambda items: self.model(**dict(items)),
            encoding='cp866',
        )

        return db


class RawDBFTable(RawTable):
    pass

