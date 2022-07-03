from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe
from markdown import markdown
from pyquery import PyQuery
from django.core.mail import send_mail
from threading import Thread
from blog import settings
from api.models import Email


# Register your models here.
# 文章管理
class ArticleAdmin(admin.ModelAdmin):
    # 封面展示

    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px;border-radius:5px;">')
        return

    get_cover.short_description = '封面'

    # 标签展示
    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list

    get_tags.short_description = '标签'

    # 标题
    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')

    get_title.short_description = '标题'

    # 编辑和删除
    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/app01/articles/{self.nid}/delete/" target="_blank">删除</a>
        """)

    get_edit_delete_btn.short_description = '操作'
    # 定义显示字段
    list_display = [get_title, get_cover, get_tags, 'category', 'look_count', 'digg_count', 'comment_count',
                    'collects_count', 'word', 'change_date', get_edit_delete_btn,
                    ]

    # 自定义动作
    # 批量计算文章字数
    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(PyQuery(markdown(obj.content)).text())
            obj.word = word
            obj.save()

    action_word.short_description = '计算文章字数'
    action_word.type = 'success'
    # 添加到actions
    actions = [action_word]


admin.site.register(Articles, ArticleAdmin)


# class MyInfoAdmin(admin.ModelAdmin):
#     list_display = ['name','job','email','site_url']
#
# admin.site.register(MyInfo,MyInfoAdmin)

admin.site.register(Tags)

admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)


# 用户信息
class UserInfoAdmin(admin.ModelAdmin):
    # 获头像
    def get_avatar(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url.url}" style="height:60px;border-radius:5px;">')
        return

    get_avatar.short_description = '头像'

    # 获取用户名
    def get_user_name(self):
        if not self.sign_status:
            return self.username
        return '****'

    get_user_name.short_description = '用户名'

    list_display = [get_user_name, 'nick_name', get_avatar, 'sign_status', 'is_superuser',
                    'date_joined', 'last_login', 'account_status']


admin.site.register(UserInfo, UserInfoAdmin)


# 广告
class AdvertAdmin(admin.ModelAdmin):
    # href自定义
    def get_href(self):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳转链接</a>""")

    get_href.short_description = '链接'

    # 图片列表  互联网图片---图片链接
    def get_img_list(self):
        # 1.解析" ; " 2.解析换行符
        html_list = self.img_list
        html_new_list = html_list.replace('；', ';').replace('\n', ';')
        img_list = html_new_list.split(';')
        htm_str = ''
        for i in img_list:
            htm_str += f'<img src="{i}" style="height:60px;border-radius:5px;margin-right:10px;">'
        return mark_safe(htm_str)

    get_img_list.short_description = '广告图组'

    # 本地图片
    def get_img(self):
        if self.img:
            return mark_safe(f"""<img src="{self.img.url}" style="height:60px;border-radius:5px;"> """)

    get_img.short_description = '上传图片'

    list_display = ['title', get_img, get_img_list, 'author', 'is_show', get_href]


admin.site.register(Advert, AdvertAdmin)


# 设置站点背景图
class MenuImgAdmin(admin.ModelAdmin):
    def get_img(self):
        if self.url:
            return mark_safe(f"""<img src="{self.url.url}" style="height:60px;border-radius:5px;"> """)

    get_img.short_description = '背景图'
    list_display = ['url', get_img]


admin.site.register(MenuImg, MenuImgAdmin)


# 页面菜单
class MenuAdmin(admin.ModelAdmin):
    add_form_template = 'simple_admin/add_form.html'
    change_form_template = 'simple_admin/add_form.html'

    def get_menu_url(self: Menu):
        lis = [f"<img src='{i.url.url}' style='height:60px;border-radius:5px;margin-right: 5px;margin-bottom: 5px;'> "
               for i in
               self.menu_url.all()]
        return mark_safe(''.join(lis))

    get_menu_url.short_description = '图组'

    list_display = ['menu_title', 'menu_title_en', 'title',
                    'abstract', 'rotation', 'abstract_time',
                    'menu_rotation', 'menu_time', get_menu_url]


admin.site.register(Menu, MenuAdmin)


# 网站导航
class NavsAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Navs, NavsAdmin)


# 网站反馈
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'status', 'processing_content']
    readonly_fields = ['email', 'content', 'status']

    # 禁用增加按钮
    # def has_add_permission(self, request):
    #     return False

    # 禁用删除按钮
    # def has_delete_permission(self, request, obj=None):
    #     return False

    # 重写保存的方法 change == true 编辑  false 添加
    def save_model(self, request, obj, form, change):
        # 添加
        if not change:
            return
        # 编辑
        email = obj.email
        content = obj.content  # 反馈内容
        obj.status = True
        processing_content = form.data.get('processing_content')  # 回复内容

        # 发送邮件
        Thread(target=send_mail, args=(
            f'[coderove]:你反馈的信息：{content} 被回复了',
            processing_content,
            settings.EMAIL_HOST_USER,
            [email, ],
            False)).start()
        Email.objects.create(
            email=email,
            content=processing_content
        )
        return super(FeedBackAdmin, self).save_model(request, obj, form, change)


admin.site.register(Feedback, FeedBackAdmin)
