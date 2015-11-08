#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django_select2.views import AutoResponseView


class FiasFakeResponseView(AutoResponseView):

    def get_queryset(self):
        return self.widget.queryset.model.objects.filter(parentguid='70bd2324-8eba-4ff1-bd31-e2dafc10779c')
