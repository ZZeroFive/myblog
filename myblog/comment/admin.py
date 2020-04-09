from django.contrib import admin
from comment.models import Comment

from myblog.cus_site import custom_site
from myblog import BaseAdmin

@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'target', 'nickname', 'href',
        'email', 'content', 'created_time'
    )
    list_display_links = []
    list_filter = ['status']
    search_fields = ['nickname', 'email']
    fields = (
        'target', 'content',
        'href','email'
    )

    def save_model(self, request, obj, form, change):
        obj.nickname = request.user
        return super(CommentAdmin, self).save_model(request, obj, form, change)
