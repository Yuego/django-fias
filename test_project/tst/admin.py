
from django.contrib import admin

from tst.models import *


class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ['//code.jquery.com/jquery-2.1.4.min.js']

admin.site.register(Item, ItemAdmin)
#admin.site.register(CachedAddress, ItemAdmin)
#admin.site.register(CachedAddressWithArea, ItemAdmin)
#admin.site.register(CachedAddressWithHouse, ItemAdmin)
#admin.site.register(NullableAddressItem, ItemAdmin)
