# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .table import Table, ParentLookupException

from dbfread import DBF, FieldParser


class ModelFieldParser(FieldParser):

    def parseC(self, field, data):
        result = FieldParser.parseC(self, field, data)

        if not result:
            return None

        return result


class DBFTable(Table):

    def __init__(self, *args, **kwargs):
        super(DBFTable, self).__init__(*args, **kwargs)

        self.related_fields = dict({
           (f.name, f.rel.to) for f in self.model._meta.get_fields()
           if f.one_to_one or f.many_to_one
        })

    def open(self, tablelist):
        return tablelist.wrapper.get_full_path(self.filename)

    def rows(self, tablelist):
        if self.deleted:
            return []

        def recfactory(items):
            items_dict = dict(items)
            for key, model in self.related_fields:
                value = items_dict.get(key, None)
                if value:
                    try:
                        items_dict[key] = model.objects.get(pk=value)
                    except model.DoesNotExist:
                        raise ParentLookupException('{0} with key `{1}`'
                                                    ' not found. Skipping house...'.format(model.__name__, value))
            return items_dict

        def fast_recfactory(items):
            items_dict = dict(items)
            for key, model in self.related_fields:
                value = items_dict.pop(key, None)
                if value:
                    items_dict['{0}_id'.format(key)] = value
            return items_dict

        db = DBF(
            self.open(tablelist=tablelist),
            lowernames=True,
            parserclass=ModelFieldParser,
            recfactory=fast_recfactory,
            encoding='cp866',
        )

        return db


