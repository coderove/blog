"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from app01.views import index,bankend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/', bankend.admin_home),
    path('', index.index),
    # path('news/', views.news),
    path('moods/', index.moods),
    path('sites/', index.sites),
    path('history/', index.history),
    path('about/', index.about),
    path('search/', index.search),

    path('login/', index.login),
    path('login/random_code/', index.get_random_code),
    path('sign/', index.sign),
    path('logout/', index.logout),
    re_path(r'^article/(?P<nid>\d+)/', index.article),  # 文章详情

    path('backend/', bankend.backend),  # 管理后台
    path('backend/add_article/', bankend.add_article),  # 添加文章
    path('backend/edit_avatar/', bankend.edit_avatar),  # 修改头像
    path('backend/rest_password/', bankend.rest_password),  # 修改密码
    path('backend/avatar_manage/', bankend.avatar_manage),  # 头像管理
    path('backend/article_cover_manage/', bankend.article_cover_manage),  # 文章封面管理

    re_path(r'^backend/edit_article/(?P<nid>\d+)', bankend.edit_article),  # 编辑文章

    re_path(r'^api/', include('api.urls')),  # 路由分发
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件
]
