#coding: utf-8
from __future__ import unicode_literals, absolute_import

try:
    from django.apps import AppConfig

    class TestAppConfig(AppConfig):
        name = 'tests.testapp'
except ImportError:
    pass
