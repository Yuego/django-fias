# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
   url(r'^suggest.json$', SphinxResponseView.as_view(), name='suggest'),
   url(r'^suggest-area.json$', GetAreasListView.as_view(), name='suggest-area'),
)
