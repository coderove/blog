from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, UserInfo, Cover, History
from api.views.login import clean_form
from django import forms
import datetime
from api.utils.power_control import is_super_method

class HistoryForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入事件标题'})
    content = forms.CharField(error_messages={'required': '请输入事件内容'})
    create_date = forms.CharField(required=False)  # 不验证是否为空
    drawing = forms.CharField(required=False)  # 不验证是否为空

    def clean_create_date(self):
        create_date = self.cleaned_data['create_date']
        if not create_date:
            create_date = datetime.date.today()
            return create_date
        date = datetime.datetime.strptime(create_date.split('T')[0], '%Y-%m-%d').date()
        return date


# 回忆录
class HistoryView(View):
    @is_super_method
    def post(self, request, **kwargs):
        res = {
            'self': None,
            'msg': '事件发布成功！',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)
        data: dict = request.data

        data['status'] = 1
        form = HistoryForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        nid = kwargs.get('nid')
        if nid:  # 编辑回忆录
            history_query = History.objects.filter(nid=nid)
            history_query.update(**form.cleaned_data)
            res['code'], res['msg'] = 0, '事件编辑成功'
            return JsonResponse(res)

        History.objects.create(**form.cleaned_data)  # 添加回忆录
        res['code'] = 0
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'msg': '事件删除成功！',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可操作！！！'
            return JsonResponse(res)
        history_query = History.objects.filter(nid=nid)
        history_query.delete()
        res['code'] = 0
        return JsonResponse(res)
