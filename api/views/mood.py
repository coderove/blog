import random
from django.views import View
from api.views.login import clean_form
from django.http import JsonResponse
from django import forms
from django.db.models import F
from app01.models import Avatars, Moods, MoodComment
from api.utils.power_control import is_super_method

class AddMoodsForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    content = forms.CharField(error_messages={'required': '请输入心情内容'})
    avatar_id = forms.CharField(required=False)  # 不验证是否为
    drawing = forms.CharField(required=False)  # 不验证是否为

    def clean_avatar_id(self):
        avatar_id = self.cleaned_data['avatar_id']
        if avatar_id:
            return avatar_id
        # 随机选择
        avatar_list = [i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id


def mood_digg(model_obj, nid):
    res = {
        'msg': '点赞成功！',
        'code': 412,
        'data': 0,
    }
    mood_query = model_obj.objects.filter(nid=nid)
    mood_query.update(digg_count=F('digg_count') + 1)
    res['data'] = mood_query.first().digg_count
    res['code'] = 0
    return JsonResponse(res)


class MoodsView(View):
    def post(self, request):
        res = {
            'self': None,
            'msg': '心情发布成功！',
            'code': 412,
        }
        data: dict = request.data
        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        Moods.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '心情删除成功！',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)

        mood_query = Moods.objects.filter(nid=nid)
        if not mood_query:
            res['msg'] = '该心情不存在'
            return JsonResponse(res)

        mood_query.delete()
        res['code'] = 0
        return JsonResponse(res)

    def put(self, request, nid):
        return mood_digg(Moods, nid)


class MoodCommentsView(View):
    def post(self, request, nid):
        res = {
            'self': None,
            'msg': '心情回复成功！',
            'code': 412,
        }
        data: dict = request.data
        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        form.cleaned_data['mood_id'] = nid
        form.cleaned_data.pop('drawing')

        MoodComment.objects.create(**form.cleaned_data)
        Moods.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)

        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '评论删除成功！',
            'code': 412,
            'data': 0,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)

        mood_id = request.data.get('mood_id')
        MoodComment.objects.filter(nid=nid).delete()

        mood_query = Moods.objects.filter(nid=mood_id)
        mood_query.update(comment_count=F('comment_count') - 1)

        res['data'] = mood_query.first().comment_count
        res['code'] = 0
        return JsonResponse(res)

    def put(self, request, nid):
        return mood_digg(MoodComment, nid)
