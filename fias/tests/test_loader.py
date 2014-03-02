#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db.utils import IntegrityError
from fias import models
from fias.importer.loader import loader, UnknownTableError
from fias.importer.loader.base import LoaderBase
from fias.importer.table import Table
from unittest import TestCase

from .mock.archive import Archive
from .mock.table import get_table_name


class TestLoaderSelector(TestCase):

    def _get_table(self, name):
        return Table(Archive(), get_table_name(name))

    def _get_loader(self, name):
        return loader(self._get_table(name))

    def test_addrobj_loader_exist(self):
        ldr = self._get_loader('addrobj')

        self.assertIsInstance(ldr, LoaderBase)

    def test_house_loader_exist(self):
        ldr = self._get_loader('house')

        self.assertIsInstance(ldr, LoaderBase)

    def test_houseint_loader_exist(self):
        ldr = self._get_loader('houseint')

        self.assertIsInstance(ldr, LoaderBase)

    def test_landmark_loader_exist(self):
        ldr = self._get_loader('landmark')

        self.assertIsInstance(ldr, LoaderBase)

    def test_normdoc_loader_exist(self):
        ldr = self._get_loader('normdoc')

        self.assertIsInstance(ldr, LoaderBase)

    def test_socrbase_loader_exist(self):
        ldr = self._get_loader('socrbase')

        self.assertIsInstance(ldr, LoaderBase)


class TestTableLoading(TestCase):

    def _get_table(self, name):
        return Table(Archive(), get_table_name(name))

    def _get_loader(self, name):
        return loader(self._get_table(name))

    def _load(self, name, truncate=False):
        ldr = self._get_loader(name)
        ldr.load(truncate=truncate)

    def test_addrobj_loading(self):
        self.assertEqual(models.AddrObj.objects.all().count(), 0)

        self._load('addrobj')

        count = models.AddrObj.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='addrobj')

        self._load('addrobj', truncate=True)

        count2 = models.AddrObj.objects.all().count()
        self.assertEqual(count, count2)

    def test_house_loading(self):
        self.assertEqual(models.House.objects.all().count(), 0)

        self._load('addrobj', truncate=True)
        self._load('house')

        count = models.House.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='house')

        self._load('house', truncate=True)

        count2 = models.House.objects.all().count()
        self.assertEqual(count, count2)

    def test_houseint_loading(self):
        self.assertEqual(models.HouseInt.objects.all().count(), 0)

        self._load('addrobj', truncate=True)
        self._load('houseint')

        count = models.HouseInt.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='houseint')

        self._load('houseint', truncate=True)

        count2 = models.HouseInt.objects.all().count()
        self.assertEqual(count, count2)

    def test_landmark_loading(self):
        self.assertEqual(models.LandMark.objects.all().count(), 0)

        self._load('addrobj', truncate=True)
        self._load('landmark')

        count = models.LandMark.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='landmark')

        self._load('landmark', truncate=True)

        count2 = models.LandMark.objects.all().count()
        self.assertEqual(count, count2)

    def test_normdoc_loading(self):
        self.assertEqual(models.NormDoc.objects.all().count(), 0)

        self._load('normdoc')

        count = models.NormDoc.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='normdoc')

        self._load('normdoc', truncate=True)

        count2 = models.NormDoc.objects.all().count()
        self.assertEqual(count, count2)

    def test_socrbase_loading(self):
        self.assertEqual(models.SocrBase.objects.all().count(), 0)

        self._load('socrbase')

        count = models.SocrBase.objects.all().count()
        self.assertNotEqual(count, 0)

        self.assertRaises(IntegrityError, self._load, name='socrbase')

        self._load('socrbase', truncate=True)

        count2 = models.SocrBase.objects.all().count()
        self.assertEqual(count, count2)
