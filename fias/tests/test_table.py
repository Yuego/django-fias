#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.table import BadTableNameError, Table
import datetime
from unittest import TestCase


from .mock.archive import Archive

_date = datetime.date(2014, 2, 22)


class TestTable(TestCase):
    _tablename = 'AS_ACTSTAT_20140222_0345ce0b-12af-482b-90f4-461b4953fe46.XML'
    _bad_tablename = 'AS_ACTSTAT_20140222_0345ce0b-12af-482b-90f4-461b4953fe46a.XML'
    _del_tablename = 'AS_DEL_ACTSTAT_20140222_0345ce0b-12af-482b-90f4-461b4953fe46.XML'

    def setUp(self):
        pass

    def test_wrong_name_raises_exception(self):
        self.assertRaises(BadTableNameError, Table, archive=Archive(), filename=self._bad_tablename)

    def test_table_parsed(self):
        table = Table(Archive(), filename=self._tablename)

        self.assertEqual(table.name,'actstat', 'Names not equal')
        self.assertFalse(table.is_deleted, 'Table deleted?')
        self.assertEqual(table.date, _date, 'Dates not equal')
        self.assertEqual(table.uuid, '0345ce0b-12af-482b-90f4-461b4953fe46', 'UUID not equal')

    def test_deleted_table_parsed(self):
        table = Table(Archive(), filename=self._del_tablename)

        self.assertTrue(table.is_deleted, 'Table not deleted?')

    def test_table_opens_self_name_from_archive(self):
        table = Table(Archive(), filename=self._tablename)

        self.assertEqual(table.open(), self._tablename, 'Different filenames!')
