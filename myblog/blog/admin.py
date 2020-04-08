from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from blog.models import Category
from blog.models import Tag
from blog.models import Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner','created_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print('{}'.format(change))
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print('{}'.format(change))
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'desc', 'content',
        'category', 'operator'
    )
    list_display_links = []
    list_filter = ['category', 'tag']
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    # 编辑页面
    save_on_top = True
    fields = (
        ('category', 'title'),
        'desc','status','content','tag'
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)