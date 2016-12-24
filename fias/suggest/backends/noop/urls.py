# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^suggest.json$', EmptyResponseListView.as_view(), name='suggest'),
    url(r'^suggest-area.json$', EmptyResponseListView.as_view(), name='suggest-area'),
]
