import time

from django.views import View
from django.http import JsonResponse
from app01.models import NavTags, Navs
from api.views.login import clean_form
from django import forms
import datetime
from urllib.parse import unquote
from django.db.models import F
from api.utils.power_control import is_super_method

# 网站导航相关视图


class NavTagsView(View):
    def post(self, request, **kwargs):
        res = {
            'self': None,
            'msg': '标签添加成功！',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)
        title = request.data.get('site_title')
        if not title:
            res['msg'] = '请输入标签名！'
            return JsonResponse(res)

        nid = kwargs.get('nid')
        if nid:
            # 编辑标签
            tag_query = NavTags.objects.filter(nid=nid)
            tag_query.update(title=title)
            res['code'], res['msg'] = 0, '标签已编辑成功！'
            return JsonResponse(res)

        # 添加标签
        tag_query = NavTags.objects.filter(title=title)
        if tag_query:
            res['msg'] = '标签已存在，请勿重新添加！'
            return JsonResponse(res)
        NavTags.objects.create(title=title)
        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '标签删除成功！',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)
        navtags_query = NavTags.objects.filter(nid=nid)
        if not navtags_query:
            res['msg'] = '标签不存在'
            return JsonResponse(res)

        navtags_query.delete()
        res['code'] = 0
        return JsonResponse(res)


# 字段验证
class NavForm(forms.Form):
    title = forms.CharField(min_length=4, error_messages={'required': '请输入网站标题', 'min_length': '网站标题最少4个字符！！！'})
    abstract = forms.CharField(min_length=10, error_messages={'required': '请输入网站简介', 'min_length': '网站简介最少10个字符！！！'})
    href = forms.URLField(error_messages={'required': '请输入网站链接'})
    icon_href = forms.URLField(error_messages={'required': '请输入网站图标链接'})
    status = forms.IntegerField(required=False)  # 不验证是否为空

    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.add_or_edit = kwargs.pop('add_or_edit', True)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        nav_query = Navs.objects.filter(title=title)
        if self.add_or_edit:
            if nav_query:
                self.add_error('title', '该标题重复，网站或已存在，请勿重复上传！！！')
        return title

    def clean_status(self):
        status = 0
        # 超级管理员
        if self.request.user.is_superuser:
            status = 1
        return status


# 获取标签下的数据
class NavView(View):
    def get(self, request):
        title = unquote(request.GET.get("title"), "UTF-8")
        order = request.GET.get('order')
        data = []

        # 判断用户是否登录
        if request.user.is_authenticated:
            nav_coll_list = request.user.navs.all()
        else:
            nav_coll_list = []

        # 我的收藏
        if title == '我的收藏' and request.user.is_authenticated:
            nav_list = request.user.navs.all().order_by(f'-{order}')
        else:
            nav_list = Navs.objects.filter(tag__title=title, status=1).order_by(f'-{order}')

        for nav in nav_list:
            data.append({
                'nid': nav.nid,
                'title': nav.title,
                'abstract': nav.abstract,
                'href': nav.href,
                'icon_href': nav.icon_href,
                'create_date': nav.create_date.strftime('%Y-%m-%d'),
                'collects_count': nav.collects_count,
                'digg_count': nav.digg_count,
                'tag': [{'nid': tag.nid, 'title': tag.title, } for tag in nav.tag.all()],
                'is_collect': 'show' if nav in nav_coll_list else '',
            })

        return JsonResponse(data, safe=False)

    def post(self, request):
        res = {
            'self': None,
            'msg': '网站添加成功！',
            'code': 412,
        }
        data = request.data
        form = NavForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 添加
        obj = Navs.objects.create(**form.cleaned_data)
        # 添加标签
        tag = data.get('tag')
        if tag:
            obj.tag.add(*tag)

        if not request.user.is_superuser:
            res['msg'] = '添加成功，管理员审核后可见！'

        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def put(self, request, nid):
        res = {
            'self': None,
            'msg': '网站编辑成功！',
            'code': 412,
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)

        data = request.data
        form = NavForm(data, request=request, add_or_edit=False)

        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 编辑
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(**form.cleaned_data)
        # 标签处理
        tag = data.get('tag')
        obj: Navs = nav_query.first()
        # 先清空再添加
        obj.tag.clear()
        if tag:
            obj.tag.add(*tag)
        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '网站删除成功！',
            'code': 412,
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)

        # 删除
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 卡片点赞

class NavDiggView(View):
    def post(self, request, nid):
        res = {
            'msg': '点赞 +1',
            'code': 412,
        }
        # 点赞时间限制
        last_time = request.session.get(f'site_{nid}', 0)
        now = int(time.time())

        if (now - last_time) < 5:
            res['msg'] = '点赞过于频繁，请不要短时间重复点赞！！！'
            return JsonResponse(res)

        request.session[f'site_{nid}'] = now

        Navs.objects.filter(nid=nid).update(digg_count=F('digg_count') + 1)
        res['code'] = 0
        return JsonResponse(res)


# 卡片收藏
class NavCollectsView(View):
    # 单个用户 只能收藏一次，第二次就取消收藏
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '网站收藏成功',
            'isCollects': True,
            'data': 0,
        }
        # 是否登录
        if not request.user.username:
            res['msg'] = '请登录后，再进行操作'
            return JsonResponse(res)
        # 判断用户是否已收藏该网站
        flag = request.user.navs.filter(nid=nid)
        num = 1
        if flag:
            # 用户已收藏--取消
            res['msg'] = '取消收藏'
            res['isCollects'] = False
            request.user.navs.remove(nid)
            num = -1
        else:
            # 添加收藏
            request.user.navs.add(nid)

        res['code'] = 0
        res['data'] = num
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(collects_count=F('collects_count') + num)

        # collects_count = nav_query.first().collects_count
        # res['data'] = collects_count

        return JsonResponse(res)


# 友链
class FriendLinks(View):
    def post(self, request):
        res = {
            'self': None,
            'msg': '友链添加成功！',
            'code': 412,
        }
        data = request.data
        form = NavForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 添加
        obj = Navs.objects.create(**form.cleaned_data)
        # 添加标签
        nav_tag = NavTags.objects.get(title='博客')
        obj.tag.add(nav_tag.nid)

        if not request.user.is_superuser:
            res['msg'] = '友链申请成功，管理员审核后可见！'

        res['code'] = 0
        return JsonResponse(res)
