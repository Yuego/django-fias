#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from django.db.models import Model

from fias.routers import FIASRouter
from fias.config import FIAS_DATABASE_ALIAS


fias = __import__('fias.models')
fias_models = ['SocrBase', 'NormDoc', 'AddrObj', 'House', 'Version', 'Status']


class TestModel(Model):
    class Meta:
        app_label = 'nofias'


class TestModel2(Model):
    class Meta:
        app_label = 'nofias'


class TestRouter(TestCase):

    def setUp(self):
        self.router = FIASRouter()
        self.models = (getattr(fias.models, attr) for attr in fias_models)
        self.rels = (getattr(fias.models, attr) for attr in FIASRouter.ALLOWED_REL)

    def test_read_db(self):
        for model in self.models:
            if issubclass(model, Model):
                self.assertEquals(FIAS_DATABASE_ALIAS, self.router.db_for_read(model))

        self.assertIsNone(self.router.db_for_read(TestModel))

    def test_write_db(self):
        for model in self.models:
            if issubclass(model, Model):
                self.assertEquals(FIAS_DATABASE_ALIAS, self.router.db_for_write(model))

        self.assertIsNone(self.router.db_for_write(TestModel))

    def test_relation(self):
        for m1 in self.models:
            for m2 in self.models:
                self.assertTrue(self.router.allow_relation(m1, m2))

        for m in self.rels:
            self.assertFalse(self.router.allow_relation(TestModel, m))
            self.assertTrue(self.router.allow_relation(m, TestModel))

        self.assertIsNone(self.router.allow_relation(TestModel, TestModel2))
        self.assertIsNone(self.router.allow_relation(TestModel2, TestModel))

    def test_syncdb(self):
        for model in self.models:
            if issubclass(model, Model):
                self.assertTrue(self.router.allow_syncdb(FIAS_DATABASE_ALIAS, model))
                self.assertFalse(self.router.allow_syncdb('default', model))

        self.assertFalse(self.router.allow_syncdb(FIAS_DATABASE_ALIAS, TestModel))
        self.assertIsNone(self.router.allow_syncdb('default', TestModel))

