#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from fias.models import Address


class AddressAdmin(admin.ModelAdmin):

    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.js']

admin.site.register(Address, AddressAdmin)