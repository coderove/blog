from django.contrib import admin
from django.urls import path, re_path

from api.views import login, article, comment, mood, user, file, api_email, history, sites,admin_data

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('sign/', login.SignView.as_view()),  # 注册
    path('get_online/', admin_data.get_online),  # 获取在线人数
    path('get_seven_data/', admin_data.get_seven_data),  # 获取7日数据
    path('article/', article.ArticleView.as_view()),  # 发布文章

    re_path(r'article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 修改文章

    re_path(r'article/cover/(?P<nid>\d+)/', article.IndexEditArticleCoverView.as_view()),  # 首页快捷修改文章封面

    re_path(r'article_pwd/(?P<nid>\d+)/', article.ArticlePwdView.as_view()),  # 查看加密文章

    re_path(r'article/comment/(?P<nid>\d+)/', comment.CommentView.as_view()),  # 发布评论
    re_path(r'^comment_digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),  # 评论点赞

    re_path(r'article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),  # 文章点赞
    re_path(r'article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),  # 文章收藏

    path('moods/', mood.MoodsView.as_view()),  # 发布心情
    re_path(r'moods/(?P<nid>\d+)/', mood.MoodsView.as_view()),  # 删除心情
    re_path(r'mood_comments/(?P<nid>\d+)/', mood.MoodCommentsView.as_view()),  # 回复心情

    path('edit_password/', user.EditPasswordView.as_view()),  # 修改密码
    path('edit_avatar/', user.EditAvatarView.as_view()),  # 修改头像

    path('upload/avatar/', file.AvatarView.as_view()),  # 上传头像
    re_path(r'upload/avatar/(?P<nid>\d+)/', file.AvatarView.as_view()),  # 删除头像

    path('upload/cover/', file.CoverView.as_view()),  # 上传封面
    re_path(r'upload/cover/(?P<nid>\d+)/', file.CoverView.as_view()),  # 删除封面

    path('send_email/', api_email.ApiEmail.as_view()),  # 发送邮件
    path('perfect_information/', user.EditUserInfoView.as_view()),  # 完善用户信息

    path('cancel_collection/', user.CancelCollection.as_view()),  # 完善用户信息

    path('paste_upload/', file.PasteUpload.as_view()),  # 回忆录 粘贴上传图片
    path('EditorPasteUpload/', file.EditorPasteUpload.as_view()),  # Editor 粘贴上传图片

    path('history/', history.HistoryView.as_view()),  # 回忆录  发布
    re_path(r'history/(?P<nid>\d+)/', history.HistoryView.as_view()),  # 回忆录  编辑 or 删除

    path('site_tag/', sites.NavTagsView.as_view()),  # 网站导航  发布标签
    path('sites/', sites.NavView.as_view()),  # 网站导航  获取标签数据
    re_path(r'site_tag/(?P<nid>\d+)/', sites.NavTagsView.as_view()),  # 网站导航  编辑标签
    re_path(r'sites/(?P<nid>\d+)/', sites.NavView.as_view()),  # 网站导航  编辑网站卡片
    re_path(r'site_digg/(?P<nid>\d+)/', sites.NavDiggView.as_view()),  # 网站导航  网站卡片点赞
    re_path(r'site_collect/(?P<nid>\d+)/', sites.NavCollectsView.as_view()),  # 网站导航  网站卡片收藏

    path('friends_links/', sites.FriendLinks.as_view()),  # 友链申请

    path('feedback/', user.FeedBackView.as_view()),  # 意见反馈

]
