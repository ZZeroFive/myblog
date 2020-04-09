from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from blog.models import Category
from blog.models import Tag
from blog.models import Post

from myblog.cus_site import custom_site


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner','created_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print('{}'.format(change))
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    # 当前登陆用户只查看自己的文章 list页面
    def get_queryset(self, request):
        queryset = super(CategoryAdmin, self).get_queryset(request)
        return queryset.filter(owner=request.user)

@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print('{}'.format(change))
        return super(TagAdmin, self).save_model(request, obj, form, change)


# 自定义过滤器
class CatgoryOwnerFIlter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    # 这一步是查询过滤器的所有List 返回value_list 展示在右侧
    def lookups(self, request, model_admin):
         return Category.objects.filter(owner=request.user).values_list('id', 'name')

    # 当不点击右侧按钮时 不触发对queryset的过滤
    # 否则将会过滤 过滤的条件自定义 自获取
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            # category_id 不能随意指代 只可以是对
            # category, category_id, comment, content, created_time, desc, id, owner, owner_id, status, tag, title进行过滤
            return queryset.filter(category=category_id)
        return queryset




@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'desc', 'content',
        'category', 'operator'
    )
    list_display_links = []
    # list_filter = ['category', 'tag']
    list_filter = [CatgoryOwnerFIlter, 'tag']
    search_fields = ['title', 'category__name']
    actions_on_top = True
    fieldsets = (
        ('基本信息',{
            'fields':('title', 'desc')
        }),
        ('文章类别',{
            'fields':('category', 'tag')
        }),
        ('正文信息',{
            'fields':('content',)
        }),
        ('状态信息',{
            'fields':('status',)
        })
    )
    #actions_on_bottom = True
    # 编辑页面
    #save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc','status','content','tag'
    # )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # 当前登陆用户只查看自己的文章
    def get_queryset(self, request):
        queryset = super(PostAdmin, self).get_queryset(request)
        return queryset.filter(owner=request.user)