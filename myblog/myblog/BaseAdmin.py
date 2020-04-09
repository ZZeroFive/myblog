
"""
重构代码 为需要自动记录User和查看当前User发布内容的AdminModel提供可复用的代码
"""

from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)