#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import SuggestAddressView

urlpatterns = patterns('',
                       url(r'^suggest', SuggestAddressView.as_view(), name='suggest'),
)
