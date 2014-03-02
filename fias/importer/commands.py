#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db.models import Min
from fias.importer.archive import Archive, DeltaArchive, BadArchiveError
from fias.importer.log import log
from fias.models import Status, Version


def load_complete_xml(path=None, truncate=False):
    kwargs = {
        'path': path,
        'version': None,
    }
    if path is None:
        latest_version = Version.objects.latest('dumpdate')
        kwargs['version'] = latest_version

    arch = Archive(**kwargs)
    arch.load(truncate=truncate)


def load_delta_xml(skip=False):
    min_version = Status.objects.aggregate(Min('ver'))['ver__min']
    if min_version is not None:
        for version in Version.objects.filter(ver__gt=min_version).order_by('ver'):
            try:
                arch = DeltaArchive(version=version)
            except BadArchiveError as e:
                if not skip:
                    raise
                else:
                    log.error(e.message)
            else:
                arch.load(truncate=False)
    else:
        log.error('Not available. Please import the data before updating')
