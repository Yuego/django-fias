# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime

from django.core.exceptions import ImproperlyConfigured

from fias.config import PROXY
from fias.importer.signals import pre_fetch_version, post_fetch_version
from fias.models import Version

wsdl_source = "http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL"


def parse_item_as_dict(item, update_all=False):
    """
    Разбор данных о версии как словаря
    """
    ver, created = Version.objects.get_or_create(
        ver=item['VersionId'],
        dumpdate=datetime.datetime.strptime(item['TextVersion'][-10:], "%d.%m.%Y").date(),
    )

    if created or update_all:
        setattr(ver, 'complete_xml_url', item['FiasCompleteXmlUrl'])
        setattr(ver, 'complete_dbf_url', item['FiasCompleteDbfUrl'])

        if hasattr(item, 'FiasDeltaXmlUrl'):
            setattr(ver, 'delta_xml_url', item['FiasDeltaXmlUrl'])
        else:
            setattr(ver, 'delta_xml_url', None)

        if hasattr(item, 'FiasDeltaDbfUrl'):
            setattr(ver, 'delta_dbf_url', item['FiasDeltaDbfUrl'])
        else:
            setattr(ver, 'delta_dbf_url', None)

        ver.save()


def parse_item_as_object(item, update_all=False):
    """
    Разбор данных о версии, как объекта
    """
    ver, created = Version.objects.get_or_create(
        ver=item.VersionId,
        dumpdate=datetime.datetime.strptime(item.TextVersion[-10:], "%d.%m.%Y").date(),
    )

    if created or update_all:
        setattr(ver, 'complete_xml_url', item.FiasCompleteXmlUrl)
        setattr(ver, 'complete_dbf_url', item.FiasCompleteDbfUrl)

        if hasattr(item, 'FiasDeltaXmlUrl'):
            setattr(ver, 'delta_xml_url', item.FiasDeltaXmlUrl)
        else:
            setattr(ver, 'delta_xml_url', None)

        if hasattr(item, 'FiasDeltaDbfUrl'):
            setattr(ver, 'delta_dbf_url', item.FiasDeltaDbfUrl)
        else:
            setattr(ver, 'delta_dbf_url', None)

        ver.save()


def iter_version_info(result):
    if hasattr(result, 'DownloadFileInfo'):
        for item in result.DownloadFileInfo:
            yield item
    else:
        for item in result:
            yield item


try:
    from zeep.client import Client
    from zeep import __version__ as zver
    z_major, z_minor, z_sub = list(map(int, zver.split('.')))

    if z_minor < 20:
        parse_func = parse_item_as_object
    elif z_minor > 20:
        parse_func = parse_item_as_dict

    client = Client(wsdl=wsdl_source)
except ImportError:
    try:
        from suds.client import Client

        parse_func = parse_item_as_dict
        client = Client(url=wsdl_source, proxy=PROXY or None)

    except ImportError:
        raise ImproperlyConfigured('Не найдено подходящей библиотеки для работы с WSDL.'
                                   ' Пожалуйста установите zeep или suds!')


def fetch_version_info(update_all=False):

    pre_fetch_version.send(object.__class__)

    result = client.service.GetAllDownloadFileInfo()
    for item in iter_version_info(result=result):
        parse_func(item=item, update_all=update_all)

    post_fetch_version.send(object.__class__)
