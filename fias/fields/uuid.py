#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django_extensions.db.fields import UUIDField


class UUIDField(UUIDField):

    def db_type(self, connection=None):
        if connection.vendor == 'postgresql':
            return 'uuid'
        return super(UUIDField, self).db_type(connection)
