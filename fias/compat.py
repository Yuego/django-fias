#coding: utf-8
from __future__ import unicode_literals, absolute_import

try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module

try:
    from urllib.request import urlretrieve
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlretrieve
    HTTPError = IOError

try:
    from django.template.base import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist
