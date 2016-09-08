# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.dispatch import receiver
from django.utils import timezone

from fias.importer.signals import *


class Timer(object):
    start = None
    end = None

    fetch_versions = None
    download = None
    unpack = None
    load = None

    @classmethod
    def full_reset(cls):
        cls.start = None
        cls.end = None
        cls.reset_counters()

    @classmethod
    def reset_counters(cls):
        cls.download = None
        cls.unpack = None
        cls.load = None

    @classmethod
    def init(cls):
        cls.full_reset()
        cls.start = timezone.now()


@receiver(pre_fetch_version)
def pre_fetch_version_callback(sender, **kwargs):
    pass


@receiver(post_fetch_version)
def post_fetch_version_callback(sender, **kwargs):
    time = timezone.now()
    print('Version info updated at {0}. Estimated time: {1}'.format(
        time,
        time - Timer.start
    ))


@receiver(pre_load)
def pre_load_callback(sender, src, **kwargs):
    pass


@receiver(post_load)
def post_load_callback(sender, wrapper, **kwargs):
    Timer.load = timezone.now()


@receiver(pre_download)
def pre_download_callback(sender, url, **kwargs):
    Timer.download = timezone.now()


@receiver(post_download)
def post_download_callback(sender, url, path, **kwargs):
    Timer.download = timezone.now() - Timer.download


@receiver(pre_unpack)
def pre_unpack_callback(sender, archive, **kwargs):
    Timer.unpack = timezone.now()


@receiver(post_unpack)
def post_unpack_callback(sender, archive, dst, **kwargs):
    Timer.unpack = timezone.now() - Timer.unpack


@receiver(pre_import_table)
def pre_import_table_callback(sender, table, **kwargs):
    pass


@receiver(post_import_table)
def post_import_table_callback(sender, table, **kwargs):
    pass


@receiver(pre_import)
def pre_import_callback(sender, version, **kwargs):
    print('Loading data v.{0} started at {1}'.format(version.ver, timezone.now()))


@receiver(post_import)
def post_import_callback(sender, version, **kwargs):
    time = timezone.now()
    print('Data v.{0} loaded at {1}'.format(version, time))
    print('Estimated time: {0}. Download: {1}. Unpack: {2}. Import: {3}'.format(
        time - Timer.start,
        Timer.download or 0,
        Timer.unpack or 0,
        time - Timer.load
    ))
    Timer.reset_counters()


@receiver(pre_update)
def pre_update_callback(sender, before, after, **kwargs):
    print('Updating from v.{0} to v.{1} started at {2}'.format(before.ver, after.ver, timezone.now()))


@receiver(post_update)
def post_update_callback(sender, before, after, **kwargs):
    time = timezone.now()
    print('Data v.{0} is updated to v.{1} at {2}'.format(before.ver, after.ver, time))
    print('Download: {1}. Unpack: {2}. Import: {3}. Total time: {0}.'.format(
        Timer.download or 0,
        Timer.unpack or 0,
        time - Timer.load,
        time - Timer.start
    ))
    Timer.reset_counters()
