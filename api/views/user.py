import time

from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from django.db.models import F
from django.contrib import auth
from app01.models import Avatars, UserInfo, Feedback
from django.shortcuts import redirect


# 字段验证
class EditPasswordForm(forms.Form):
    old_pwd = forms.CharField(min_length=4, error_messages={'required': '请输入原密码', 'min_length': '密码长度最低4位'})
    pwd = forms.CharField(min_length=4, error_messages={'required': '请输入新的密码', 'min_length': '密码长度最低4位'})
    re_pwd = forms.CharField(min_length=4, error_messages={'required': '请确认输入密码', 'min_length': '密码长度最低4位'})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_old_pwd(self):
        old_pwd = self.cleaned_data['old_pwd']
        user = auth.authenticate(username=self.request.user.username, password=old_pwd)
        if not user:
            self.add_error('old_pwd', '原密码错误，请重新输入')
        return old_pwd

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')

        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致，请重新输入')
        return self.cleaned_data


# 修改密码
class EditPasswordView(View):
    def post(self, request):
        res = {
            'self': None,
            'msg': '密码修改成功',
            'code': 412,
        }
        data = request.data
        form = EditPasswordForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        user = request.user
        user.set_password(data['pwd'])
        user.save()
        auth.logout(request)  # 修改密码后，退出登录
        res['code'] = 0
        return JsonResponse(res)


# 修改头像
class EditAvatarView(View):
    def put(self, request):
        res = {
            'code': 424,
            'msg': '头像修改成功',
        }
        avatar_id = request.data.get('avatar_id')
        avatar = Avatars.objects.get(nid=avatar_id)
        # 判断用户的注册状态
        user = request.user
        sign_status = user.sign_status
        if sign_status == 0:
            # 用户名注册
            user.avatar_id = avatar_id
        else:
            avatar_url = avatar.url.url
            user.avatar_url = avatar_url

        user.save()

        res['code'] = 0
        res['data'] = avatar.url.url
        return JsonResponse(res)


# 完善用户信息--字段验证
class EditUserInfoForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确的邮箱'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == self.request.session.get('valid_email_obj')['email']:
            return email
        self.add_error('email', '邮箱校验错误！')

    def clean_pwd(self):
        pwd = self.cleaned_data.get('pwd')
        user = auth.authenticate(username=self.request.user.username, password=pwd)
        if user:
            return pwd
        self.add_error('pwd', '密码错误！')

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code == self.request.session.get('valid_email_obj')['code']:
            return code
        self.add_error('code', '验证码错误！')


# 完善用户信息
class EditUserInfoView(View):
    def put(self, request):
        res = {
            'self': None,
            'msg': '信息绑定成功！',
            'code': 412,
        }
        # 校验时间 防止暴力破解验证码
        valid_email_obj = request.session.get('valid_email_obj')
        if not valid_email_obj:
            res['msg'] = '请获取验证码后进行此操作！'
            return JsonResponse(res)

        old_time = valid_email_obj['time_stamp']
        now = time.time()
        if (now - old_time) >= 300:
            res['msg'] = '验证码已失效，请重新获取！'
            return JsonResponse(res)

        form = EditUserInfoForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 绑定信息
        user = request.user
        user.email = form.cleaned_data['email']
        user.save()
        res['code'] = 0
        return JsonResponse(res)


# 取消收藏
class CancelCollection(View):
    def post(self, request):
        nid_list = request.POST.getlist('nid')
        request.user.collects.remove(*nid_list)
        return redirect('/backend/')


# 反馈校验
class FeedBackForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入反馈邮箱', 'invalid': '请输入正确的邮箱'})
    content = forms.CharField(error_messages={'required': '请输入反馈内容'})


# 意见反馈
class FeedBackView(View):
    def post(self, request):
        res = {
            'code': 424,
            'msg': '感谢您的反馈，博主将尽快处理！',
            'self': None,
        }
        form = FeedBackForm(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 反馈成功
        Feedback.objects.create(**form.cleaned_data)

        res['code'] = 0
        return JsonResponse(res)
