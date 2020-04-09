from django.contrib import admin

from config.models import Link
from config.models import SiderBar
from myblog.cus_site import custom_site


@admin.register(Link, site = custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'href', 'status',
        'weight','owner'
    )

    list_display_links = []
    list_filter = ['status']
    search_fields = ['title', 'weight']
    fields = (
        'title', 'href',
        'weight'
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SiderBar, site = custom_site)
class SiderBarAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_type', 'status',
        'content','owner', 'created_time'
    )

    list_display_links = []
    list_filter = ['status']
    search_fields = ['title']
    fields = (
        'title', 'display_type',
        'content'
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)
