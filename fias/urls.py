#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from fias.views import SuggestAddressView, GetAreasListView

urlpatterns = patterns('',
                       url(r'^suggest', SuggestAddressView.as_view(), name='suggest'),
                       url(r'^get_areas_list', GetAreasListView.as_view(), name='get_areas_list'),
)
