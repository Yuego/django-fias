# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module
from fias.config import SUGGEST_BACKEND

try:
    backend = import_module('%s.backend' % SUGGEST_BACKEND)
except ImportError:

    raise ImproperlyConfigured('Suggest backend `{0}` does not exists'.format(SUGGEST_BACKEND))
