# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import ImproperlyConfigured

from fias.compat import import_module
from fias.config import SUGGEST_BACKEND

try:
    backend = import_module('%s.backend' % SUGGEST_BACKEND)
except ImportError:

    raise ImproperlyConfigured('Suggest backend `{0}` does not exists'.format(SUGGEST_BACKEND))
