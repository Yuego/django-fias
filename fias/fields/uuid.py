# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import ImproperlyConfigured
try:
    from django.db.models import UUIDField
except ImportError:
    try:
        from django_extensions.db.fields import UUIDField as UF

        class UUIDField(UF):

            def __init__(self, *args, **kwargs):
                kwargs['auto'] = False
                super(UUIDField, self).__init__(*args, **kwargs)

            def db_type(self, connection=None):
                if connection.vendor == 'postgresql':
                    return 'uuid'
                return super(UUIDField, self).db_type(connection)

        # MonkeyPatch...
        from django.db import models
        models.UUIDField = UUIDField

    except ImportError:
        raise ImproperlyConfigured('You must use Django 1.8+ or install `django_extensions` package')
