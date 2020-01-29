from django.contrib import admin

from .models import LinkBox


class LinkBoxAdmin(admin.ModelAdmin):
    list_display = ('owner', 'boxname', 'created')
    list_filter = ('owner',)


admin.site.register(LinkBox, LinkBoxAdmin)
