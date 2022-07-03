from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from app01.models import Comment, Articles
from django.db.models import F
from api.utils.find_root_comment import find_root_comment
from app01.utils.sub_comment import find_root_sub_comment


# 评论操作
class CommentView(View):
    # 发布评论
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '文章评论发布成功',
            'self': None,
        }
        # 文章id 用户 评论内容
        data = request.data
        # 是否登录
        if not request.user.username:
            res['msg'] = '请登录后，再发布评论'
            return JsonResponse(res)

        # 校验是否有文章内容
        content = data.get('content')
        if not content:
            res['self'], res['msg'] = 'content', '请先输入内容，再发布评论'
            return JsonResponse(res)

        # 校验成功
        pid = data.get('pid')
        if pid:
            comment_obj = Comment.objects.create(content=content, user=request.user, article_id=nid,
                                                 parent_comment_id=pid)
            # 根评论数+1
            # 找到最上级的root
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
        else:
            # 根评论
            Comment.objects.create(content=content, user=request.user, article_id=nid)

        # 文章评论数+1
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        res['code'] = 0
        return JsonResponse(res)

    # 删除评论
    def delete(self, request, nid):
        # 权限 发布评论的人或者管理员
        res = {
            'code': 412,
            'msg': "评论删除成功！",
        }
        # 文章id
        aid = request.data.get('aid')
        # root评论id
        pid = request.data.get('pid')
        # 当前登录用户
        login_user = request.user
        # 评论发布人
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user
        # 删除验证
        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = "无权限删除此评论"
            return JsonResponse(res)
        # 删除的是根评论
        # 获得子评论数量
        lis = []
        find_root_sub_comment(comment_query.first(), lis)
        # 文章评论数
        Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis) - 1)
        if pid:
            # 评论数-1   子评论
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - len(lis) - 1)

        # 删除评论-子评论
        comment_query.delete()
        res['code'] = 0
        return JsonResponse(res)


# 评论点赞
class CommentDiggView(View):
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '点赞成功',
            'data': 0,
        }
        # 是否登录
        if not request.user.username:
            res['msg'] = '请登录后，再点赞'
            return JsonResponse(res)
        comment_query = Comment.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        digg_count = comment_query.first().digg_count
        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)
