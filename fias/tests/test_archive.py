#coding: utf-8
from __future__ import unicode_literals, absolute_import


from fias.importer.archive import Archive
from fias.importer.table import Table
from fias.importer.version import update_versions
from unittest import TestCase

_test_archive = 'fias/tests/data/fias.rar'


class TestLocalArchive(TestCase):

    def setUp(self):
        update_versions(update_all=True)
        self._archive = Archive(path=_test_archive)

    def test_archive_returns_table_list(self):
        tables = self._archive.tables

        self.assertIsInstance(tables, dict)
        self.assertTrue(len(tables) > 0)
        self.assertIsInstance(tables.items()[0][1], Table)
