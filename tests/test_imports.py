# coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase
from importlib import import_module
import types


class TestImports(TestCase):

    def _import(self, path):
        return import_module(path)

    def test_fields(self):
        self.assertIsInstance(self._import('fias.fields'), types.ModuleType)

    def test_importer_source(self):
        self.assertIsInstance(self._import('fias.importer.source'), types.ModuleType)

    def test_importer_table(self):
        self.assertIsInstance(self._import('fias.importer.table'), types.ModuleType)

    def test_importer(self):
        self.assertIsInstance(self._import('fias.importer'), types.ModuleType)

    def test_management_fias(self):
        self.assertIsInstance(self._import('fias.management.commands.fias'), types.ModuleType)

    def test_management_fias_suggest(self):
        self.assertIsInstance(self._import('fias.management.commands.fias_suggest'), types.ModuleType)

    def test_management_fiasinfo(self):
        self.assertIsInstance(self._import('fias.management.commands.fiasinfo'), types.ModuleType)

    def test_models(self):
        self.assertIsInstance(self._import('fias.models'), types.ModuleType)

    def test_suggest(self):
        self.assertIsInstance(self._import('fias.suggest'), types.ModuleType)

    def test_suggest_backend_noop(self):
        self.assertIsInstance(self._import('fias.suggest.backends.noop'), types.ModuleType)

    def test_suggest_backend_sphinx(self):
        self.assertIsInstance(self._import('fias.suggest.backends.sphinx'), types.ModuleType)

    def test_admin(self):
        self.assertIsInstance(self._import('fias.admin'), types.ModuleType)

    def test_forms(self):
        self.assertIsInstance(self._import('fias.forms'), types.ModuleType)

    def test_routers(self):
        self.assertIsInstance(self._import('fias.routers'), types.ModuleType)

    def test_views(self):
        self.assertIsInstance(self._import('fias.views'), types.ModuleType)
