#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from fias.views import *

urlpatterns = patterns('',
   url(r'^auto.json', FiasFakeResponseView.as_view(), name='json'),
)
