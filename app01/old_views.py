# from django.shortcuts import render, HttpResponse, redirect
# from django.http import JsonResponse
# from app01.utils.pictureVerifCode import random_code
# from django import forms
# from django.contrib import auth
# from app01.models import *
# from app01.utils.sub_comment import sub_comment_list
# from app01.utils.pageInation import PageInation
# from django.db.models import F
#
#
# # import urllib.parse
#
#
# # Create your views here.
# # 首页
# def index(request):
#     article_list = Articles.objects.filter(status=1).order_by('-change_date')
#     front_end_list = article_list.filter(category=1)[:6]
#     end_front_list = article_list.filter(category=2)[:6]
#
#     query_params = request.GET.copy()
#     # 分页器
#     """
#             :param current_page:当前页码
#             :param all_count: 数据库总条数
#             :param base_url:原始url
#             :param query_params:保留原搜索条件
#             :param per_page:一页展示多少条
#             :param pager_page_count:最多显示多少个页码
#     """
#     pager = PageInation(
#         current_page=request.GET.get('page'),
#         all_count=article_list.count(),
#         base_url=request.path_info,
#         query_params=query_params,
#         per_page=2,
#         pager_page_count=7
#     )
#     article_list = article_list[pager.start:pager.end]
#     # 个性化展示
#     advert_list = Advert.objects.filter(is_show=True)
#
#     return render(request, 'index.html', locals())
#
#
# # 全文检索
# def search(request):
#     # 获取请求路径
#     query_params = request.GET.copy()
#     # 搜索关键字
#     search_key = request.GET.get('key', '')
#     # 排序依据
#     order = request.GET.get('order', '')
#     # 标签依据
#     tag = request.GET.get('tag', '')
#     # 字数依据
#     word = request.GET.getlist('word')
#     # 数据检索
#     article_list = Articles.objects.filter(title__contains=search_key)
#
#     # 字数过滤
#     if len(word) == 2:
#         article_list = article_list.filter(word__range=word)
#     # 标签
#     if tag:
#         article_list = article_list.filter(tag__title=tag)
#
#     # 排序判断
#     if order:
#         try:
#             article_list = article_list.order_by(order)
#         except  Exception:
#             pass
#
#             # 分页器
#     pager = PageInation(
#         current_page=request.GET.get('page'),
#         all_count=article_list.count(),
#         base_url=request.path_info,
#         query_params=query_params,
#         per_page=10,
#         pager_page_count=7,
#     )
#     article_list = article_list[pager.start:pager.end]
#
#     # 文章搜索
#     return render(request, 'search.html', locals())
#
#
# # 文章
# def article(request, nid):
#     article_query = Articles.objects.filter(nid=nid)
#     # 浏览量+1
#     article_query.update(look_count=F('look_count') + 1)
#     if not article_query:
#         return redirect('/')
#     article = article_query.first()
#     # 评论
#     comment_list = sub_comment_list(nid)
#     return render(request, 'article.html', locals())
#
#
# # 新闻
# # def news(request):
# #     return render(request, 'news.html')
#
# #  心情
# def moods(request):
#     avatar_list = Avatars.objects.all()
#     # 搜索
#     key = request.GET.get('key', '')
#
#     mood_list = Moods.objects.filter(content__contains=key).order_by('-create_date')
#     # 分页器
#     # 获取请求路径
#     query_params = request.GET.copy()
#     pager = PageInation(
#         current_page=request.GET.get('page'),
#         all_count=mood_list.count(),
#         base_url=request.path_info,
#         query_params=query_params,
#         per_page=5,
#         pager_page_count=7,
#     )
#     mood_list = mood_list[pager.start:pager.end]
#     return render(request, 'moods.html', locals())
#
#
# #  回忆录
# def history(request):
#     return render(request, 'history.html', locals())
#
#
# #  网站导航
# def sites(request):
#     return render(request, 'sites.html', locals())
#
#
# #  关于
# def about(request):
#     return render(request, 'about.html', locals())
#
#
# # 验证码
# def get_random_code(request):
#     data, valid_code = random_code()
#     request.session['valid_code'] = valid_code
#     return HttpResponse(data)
#
#
# # 登录
# def login(request):
#     return render(request, 'login.html')
#
#
# # 注册
# def sign(request):
#     return render(request, 'sign.html')
#
#
# # 注销退出
# def logout(request):
#     auth.logout(request)
#     return redirect('/')
#
#
# # 后台系统
# def backend(request):
#     # 未登录
#     if not request.user.username:
#         return redirect('/')
#     return render(request, 'backend/backend.html', locals())
#
#
# # 文章
# def add_article(request):
#     # 所有文章分类
#     category_list = Articles.category_choice
#     # 获取所有的分类、标签
#     tag_list = Tags.objects.all()
#     # 获取所有的文章封面
#     cover_list = Cover.objects.all()
#     c_l = []
#     for cover in cover_list:
#         # url = urllib.parse.unquote(cover.url.url)
#         c_l.append({
#             'url': cover.url.url,
#             'nid': cover.nid
#         })
#     return render(request, 'backend/add_article.html', locals())
#
#
# # 编辑文章
# def edit_article(request, nid):
#     # 所有文章分类
#     category_list = Articles.category_choice
#     # 获取所有的分类、标签
#     tag_list = Tags.objects.all()
#     # 获取所有的文章封面
#     cover_list = Cover.objects.all()
#     c_l = []
#     for cover in cover_list:
#         c_l.append({
#             'url': cover.url.url,
#             'nid': cover.nid
#         })
#     article_obj = Articles.objects.get(nid=nid)
#     tags = [str(tag.nid) for tag in article_obj.tag.all()]
#     return render(request, 'backend/edit_article.html', locals())
#
#
# # 修改头像
# def edit_avatar(request):
#
#     avatar_list = Avatars.objects.all()
#     user = request.user
#     sign_status = user.sign_status
#     if sign_status==0:
#         avatar_id = request.user.avatar.nid
#     else:
#         avatar_url = request.user.avatar.url.url
#         for i in avatar_list:
#             if i.url.url == avatar_url:
#                 avatar_id = i.nid
#     return render(request, 'backend/edit_avatar.html', locals())
#
#
# # 重置密码
# def rest_password(request):
#     return render(request, 'backend/rest_password.html', locals())
