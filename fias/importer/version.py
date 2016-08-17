# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from fias.importer.signals import pre_fetch_version, post_fetch_version
from fias.models import Version


wsdl_source = "http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL"
try:
    from zeep.client import Client



    def fetch_version_info(update_all=False):
        pre_fetch_version.send(object.__class__)

        client = Client(wsdl=wsdl_source)
        result = client.service.GetAllDownloadFileInfo()

        for item in result.DownloadFileInfo:
            try:
                ver = Version.objects.get(ver=item.VersionId)
            except Version.DoesNotExist:
                ver = Version(**{
                    'ver': item.VersionId,
                    'dumpdate': datetime.datetime.strptime(item.TextVersion[-10:], "%d.%m.%Y").date(),
                })
            finally:
                if not ver.pk or update_all:
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

        post_fetch_version.send(object.__class__)
except ImportError:
    from suds.client import Client


    def fetch_version_info(update_all=False):
        pre_fetch_version.send(object.__class__)

        client = Client(url=wsdl_source)
        result = client.service.GetAllDownloadFileInfo()

        for item in result.DownloadFileInfo:
            try:
                ver = Version.objects.get(ver=item['VersionId'])
            except Version.DoesNotExist:
                ver = Version(**{
                    'ver': item['VersionId'],
                    'dumpdate': datetime.datetime.strptime(item['TextVersion'][-10:], "%d.%m.%Y").date(),
                })
            finally:
                if not ver.pk or update_all:
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

        post_fetch_version.send(object.__class__)
