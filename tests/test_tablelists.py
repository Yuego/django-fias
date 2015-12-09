# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os
from django.test import TestCase

from fias.importer.source.tablelist import TableList
from fias.importer.source import *
from fias.models import Version

from .info import FAKE_FILES
from .mock.wrapper import Wrapper


class TestTableList(TestCase):
    original_wrapper = None

    def setUp(self):
        self.original_wrapper = TableList.wrapper_class
        TableList.wrapper_class = Wrapper

    def tearDown(self):
        TableList.wrapper_class = self.original_wrapper

    def test_version_type(self):
        self.assertRaises(AssertionError, TableList, src=None, version=type('NotAVersion'))

        ver = Version(ver=0, dumpdate=datetime.datetime.today())

        tl = TableList(src=None, version=ver)
        self.assertEqual(tl.dump_date, ver.dumpdate)

    def test_get_table_list(self):
        tl = TableList(src=None)
        self.assertEqual(set(FAKE_FILES), set(tl.get_table_list()))

    def test_get_date_info(self):
        tl = TableList(src=None)
        for f in FAKE_FILES:
            self.assertEqual(datetime.date(2000, 1, int(f[-1])+1), tl.get_date_info(f))

    def test_open(self):
        tl = TableList(src=None)
        for f in FAKE_FILES:
            fd = tl.open(f)
            self.assertEqual(os.path.basename(fd.name), f)
            fd.close()
