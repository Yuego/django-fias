#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from fias.views import *

urlpatterns = patterns('',
   url(r'^auto.json$', SphinxResponseView.as_view(), name='json'),
   url(r'^get_areas_list.json$', GetAreasListView.as_view(), name='get_areas_list'),
)
