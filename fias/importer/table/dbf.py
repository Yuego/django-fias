# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .table import Table

from dbfread import DBF, FieldParser


class ModelFieldParser(FieldParser):

    def parseC(self, field, data):
        result = FieldParser.parseC(self, field, data)

        if not result:
            return None

        return result


class DBFTable(Table):

    def open(self, tablelist):
        return tablelist.wrapper.get_full_path(self.filename)

    def rows(self, tablelist):
        if self.deleted:
            return []

        db = DBF(
            self.open(tablelist=tablelist),
            lowernames=True,
            parserclass=ModelFieldParser,
            recfactory=lambda items: self.model(**dict(items)),
            encoding='cp866',
        )

        return db


