import datetime

from django.shortcuts import render, redirect
from app01.models import *
from api.utils.power_control import is_super_fun
from api.models import *

# import urllib.parse

# Create your views here.

# 后台系统
def backend(request):
    # 未登录
    if not request.user.username:
        return redirect('/')
    # 用户收藏的所有文章
    user = request.user
    collection_query = user.collects.all()

    return render(request, 'backend/backend.html', locals())


# 添加文章
@is_super_fun
def add_article(request):
    # 所有文章分类
    category_list = Articles.category_choice
    # 获取所有的分类、标签
    tag_list = Tags.objects.all()
    # 获取所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        # url = urllib.parse.unquote(cover.url.url)
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    return render(request, 'backend/add_article.html', locals())


# 编辑文章
@is_super_fun
def edit_article(request, nid):
    # 所有文章分类
    category_list = Articles.category_choice
    # 获取所有的分类、标签
    tag_list = Tags.objects.all()
    # 获取所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid
        })
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    return render(request, 'backend/edit_article.html', locals())


# 修改头像
def edit_avatar(request):
    avatar_list = Avatars.objects.all()
    user = request.user
    sign_status = user.sign_status
    if sign_status == 0:
        avatar_id = request.user.avatar.nid
    else:
        avatar_url = request.user.avatar.url.url
        for i in avatar_list:
            if i.url.url == avatar_url:
                avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


# 重置密码
def rest_password(request):
    return render(request, 'backend/rest_password.html', locals())


# 头像管理  --上传
@is_super_fun
def avatar_manage(request):
    avatar_query = Avatars.objects.all()
    return render(request, 'backend/avatar_manage.html', locals())


# 文章封面管理 --上传
@is_super_fun
def article_cover_manage(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/article_cover_manage.html', locals())


@is_super_fun
def admin_home(request):
    # 用户总数
    user_count = UserInfo.objects.count()
    articles_count = Articles.objects.count()
    navs_count = Navs.objects.count()
    moods_count = Moods.objects.count()
    friend_link_count = Navs.objects.filter(tag__title='博客').count()
    email_count = Email.objects.count()
    # 今日注册
    now = datetime.date.today()
    today_sign=UserInfo.objects.filter(date_joined__gte=now).count()

    return render(request, 'admin_home.html', locals())
