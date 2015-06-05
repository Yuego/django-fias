#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import ImproperlyConfigured
try:
    from django.db.models import UUIDField
except ImportError:
    from django_extensions.db.fields import UUIDField as uf

    class UUIDField(uf):

        def __init__(self, verbose_name=None, name=None, auto=False, version=4, node=None, clock_seq=None, namespace=None, uuid_name=None, *args, **kwargs):
            super(UUIDField, self).__init__(verbose_name=verbose_name, name=name, auto=auto, version=version, node=node, clock_seq=clock_seq, namespace=namespace, uuid_name=uuid_name, *args, **kwargs)

        def db_type(self, connection=None):
            if connection.vendor == 'postgresql':
                return 'uuid'
            return super(UUIDField, self).db_type(connection)


except ImportError:
    raise ImproperlyConfigured('You must use Django 1.8+ or install `django_extensions` package')



