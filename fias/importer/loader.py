#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.importer.file import File, DeltaFile
from fias.models import Status, Version


def load_complete_xml(path=None, truncate=False):
    kwargs = {
        'path': path,
        'version': None,
    }
    if path is None:
        latest_version = Version.objects.latest('dumpdate')
        kwargs['version'] = latest_version

    file_ = File(**kwargs)
    file_.load(truncate)


def load_delta_xml(version):
    file_ = DeltaFile(version=version)
    file_.load()
