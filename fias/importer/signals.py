# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.dispatch import Signal

pre_fetch_version = Signal(providing_args=[])
post_fetch_version = Signal(providing_args=[])

pre_download = Signal(providing_args=['url'])
post_download = Signal(providing_args=['url', 'path'])

pre_unpack = Signal(providing_args=['archive'])
post_unpack = Signal(providing_args=['archive', 'dst'])

pre_load = Signal(providing_args=['src'])
post_load = Signal(providing_args=['wrapper'])

pre_drop_indexes = Signal(providing_args=['table'])
post_drop_indexes = Signal(providing_args=['table'])

pre_restore_indexes = Signal(providing_args=['table'])
post_restore_indexes = Signal(providing_args=['table'])

pre_import_table = Signal(providing_args=['table'])
post_import_table = Signal(providing_args=['table'])

pre_import = Signal(providing_args=['msg'])
post_import = Signal(providing_args=['msg'])

pre_update = Signal(providing_args=['before', 'after'])
post_update = Signal(providing_args=['before', 'after'])
