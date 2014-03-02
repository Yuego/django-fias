#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.table import BadTableNameError, Table
import datetime
from rarfile import PipeReader
from unittest import TestCase


from .mock.archive import Archive
from .mock.table import get_table_date, get_table_uuid, get_table_name, get_bad_table_name
_date = datetime.date(2014, 2, 22)


class TestTable(TestCase):

    def test_wrong_name_raises_exception(self):
        self.assertRaises(BadTableNameError, Table, archive=Archive(), filename=get_bad_table_name())

    def test_table_parsed(self):
        table = Table(Archive(), filename=get_table_name('table'))

        self.assertEqual(table.name, 'table', 'Names not equal')
        self.assertFalse(table.is_deleted, 'Table deleted?')
        self.assertEqual(table.date, get_table_date(), 'Dates not equal')
        self.assertEqual(table.uuid, get_table_uuid(), 'UUID not equal')

    def test_deleted_table_parsed(self):
        table = Table(Archive(), filename=get_table_name('del_table'))

        self.assertTrue(table.is_deleted, 'Table not deleted?')

    def test_table_opens_file_from_archive(self):
        table = Table(Archive(), filename=get_table_name('addrobj'))

        self.assertIsInstance(table.open(), PipeReader)
