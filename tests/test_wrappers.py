# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os
import pytest
import rarfile
import shutil
import tempfile

from django.test import TestCase

from fias.importer.source.wrapper import (
    SourceWrapper,
    DirectoryWrapper,
    RarArchiveWrapper,
)
from .info import FAKE_DIR_PATH, FAKE_ARCHIVE_PATH, FAKE_FILES

class TestSourceWrapper(TestCase):

    def setUp(self):
        self.wrapper = SourceWrapper(None)

    def test_getting_date_info(self):
        self.assertRaises(NotImplementedError, self.wrapper.get_date_info, filename=None)

    def test_getting_file_list(self):
        self.assertRaises(NotImplementedError, self.wrapper.get_file_list)

    def test_opening_file(self):
        self.assertRaises(NotImplementedError, self.wrapper.open, filename=None)


class TestDirectoryWrapper(TestCase):


    def setUp(self):
        self.wrapper = DirectoryWrapper(FAKE_DIR_PATH)

    def test_getting_file_list(self):
        filelist = self.wrapper.get_file_list()

        self.assertEqual(set(filelist), set(FAKE_FILES))

    def test_getting_date_info(self):
        date_info = self.wrapper.get_date_info(FAKE_FILES[0])

        self.assertIsInstance(date_info, datetime.date)

    def test_opening_file(self):
        filename = FAKE_FILES[0]
        fd = self.wrapper.open(filename=filename)

        self.assertEqual(os.path.basename(fd.name), filename)

        data = fd.read()

        self.assertEqual(data.decode('utf-8'), filename)


class TestTemporaryDirectoryWrapper(TestCase):

    def setUp(self):
        tmp = tempfile.mktemp()
        shutil.copytree(FAKE_DIR_PATH, tmp)

        self.wrapper = DirectoryWrapper(tmp, is_temporary=True)

    def test_deleting_temporary_data(self):
        source = self.wrapper.source
        self.assertTrue(os.path.exists(source))

        del self.wrapper

        self.assertFalse(os.path.exists(source))


class TestArchiveWrapper(TestDirectoryWrapper):

    def setUp(self):
        self.wrapper = RarArchiveWrapper(rarfile.RarFile(FAKE_ARCHIVE_PATH))

