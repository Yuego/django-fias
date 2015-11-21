#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from fias.importer.archive import Archive
from fias.importer.table import Table
from fias.importer.version import fetch_version_info
import pytest

from .mock.archive import test_archive


@pytest.mark.django_db(transaction=True)
class TestLocalArchive(TestCase):

    def setUp(self):
        fetch_version_info(update_all=True)
        self._archive = Archive(path=test_archive)

    def test_archive_returns_table_list(self):
        tables = self._archive.tables

        self.assertIsInstance(tables, dict)
        self.assertTrue(len(tables) > 0)
        self.assertIsInstance(list(tables.values())[0], Table)
