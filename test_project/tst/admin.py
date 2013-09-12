
from django.contrib import admin

from tst.models import Item

class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.js']

admin.site.register(Item, ItemAdmin)
