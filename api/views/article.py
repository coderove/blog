import random
from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from api.views.login import clean_form
from django import forms
from app01.models import Tags, Articles, Cover
from django.db.models import F
from api.utils.power_control import is_super_method


class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不验证是否为空
    cover_id = forms.IntegerField(required=False)  # 不验证是否为

    category = forms.IntegerField(required=False)  # 不验证是否为空
    word = forms.IntegerField(required=False)  # 不验证是否为空
    pwd = forms.CharField(required=False)  # 不验证是否为空
    pwd_activity = forms.BooleanField(required=False)  # 不验证是否为空
    recommend = forms.BooleanField(required=False)  # 不验证是否为空

    status = forms.IntegerField(required=False)  # 不验证是否为空

    # 字数统计
    def clean_word(self):
        word = self.cleaned_data['word']
        word = len(PyQuery(markdown(self.cleaned_data.get('content'))).text())
        return word

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
            # 截取正文前90个字符作为文章简介
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_dict = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_dict)['nid']
        return cover_id


# 添加标签
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            # 创建新标签
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


class ArticleView(View):
    # 添加文章
    @is_super_method
    def post(self, request):
        res = {
            'data': None,
            'msg': '文章发布成功！',
            'code': 412,
        }
        data: dict = request.data

        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 校验通过
        form.cleaned_data['author'] = 'coderove'
        form.cleaned_data['source'] = 'coderove个人博客'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags, article_obj)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    @is_super_method
    def put(self, request, nid):
        res = {
            'data': None,
            'msg': '文章编辑成功！',
            'code': 412,
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误！'
            return JsonResponse(res)

        data: dict = request.data
        data['status'] = 1

        # 清除残留密码数据
        if not data['pwd_activity']:
            data['pwd'] = ''

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 校验通过
        form.cleaned_data['author'] = 'coderove'
        form.cleaned_data['source'] = 'coderove个人博客'
        article_query.update(**form.cleaned_data)

        tags = data.get('tags')
        # 标签修改
        # 1.清空所有标签
        article_query.first().tag.clear()
        # 添加标签
        add_article_tags(tags, article_query.first())
        # 校验文章密码
        # if not article_query.first().pwd_activity:

        res['code'] = 0
        res['data'] = article_query.first().nid

        return JsonResponse(res)


# 文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '点赞成功',
            'data': 0,
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        digg_count = comment_query.first().digg_count
        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectsView(View):
    # 单个用户 只能收藏一次，第二次就取消收藏
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '收藏成功',
            'isCollects': True,
            'data': 0,
        }
        # 是否登录
        if not request.user.username:
            res['msg'] = '请登录后，再收藏'
            return JsonResponse(res)
        # 判断用户是否已收藏该文章
        flag = request.user.collects.filter(nid=nid)
        num = 1
        if flag:
            # 用户已收藏--取消
            res['msg'] = '取消收藏'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            # 添加收藏
            request.user.collects.add(nid)
        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count
        res['code'], res['data'] = 0, collects_count
        return JsonResponse(res)


# 加密文章查看
class ArticlePwdView(View):
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '您已获得访问权限！！！',
        }
        pwd = request.data.get('pwd')
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '文章不存在！！！'
            return JsonResponse(res)

        article_obj = article_query.first()
        if article_obj.pwd != pwd:
            res['msg'] = '权限码错误或已过期！'
            return JsonResponse(res)

        request.session[f'article_pwd__{nid}'] = pwd

        res['code'] = 0
        return JsonResponse(res)


# 首页快捷修改文章封面
class IndexEditArticleCoverView(View):
    @is_super_method
    def post(self, request, nid):
        if not request.user.is_superuser:
            return JsonResponse({})
        cid = request.data.get('nid')
        Articles.objects.filter(nid=nid).update(cover_id=cid)
        return JsonResponse({})
