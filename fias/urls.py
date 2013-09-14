#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from fias.views import (SuggestAddressViewStepByStep,
                        SuggestBySphinx,
                        GetAreasListView)

urlpatterns = patterns('',
                       url(r'^suggest_sbs', SuggestAddressViewStepByStep.as_view(), name='suggest_step_by_step'),
                       url(r'^suggest_sphinx', SuggestBySphinx.as_view(), name='suggest_by_sphinx'),
                       url(r'^get_areas_list', GetAreasListView.as_view(), name='get_areas_list'),
)
