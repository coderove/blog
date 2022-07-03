from django import forms
from django.contrib import auth
from app01.models import UserInfo, Avatars
from django.views import View
from django.http import JsonResponse
import random


# 登录注册base类
class LoginBaseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码错误')
        return self.cleaned_data


# 登录字段验证
class LoginForm(LoginBaseForm):
    # 全局勾子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')

        user = auth.authenticate(username=name, password=pwd)
        error_count = self.request.session.get('error_count', 0)

        # 登录用户名或密码错误次数
        if error_count >= 3:
            self.add_error('name', '验证码已失效，请重新获取！')
            return None

        # 用户名或密码错误
        if not user:
            error_count += 1
            self.request.session['error_count'] = error_count

            self.add_error('name', '用户名或密码错误')
            return self.cleaned_data

        self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册字段验证
class SignForm(LoginBaseForm):
    re_pwd = forms.CharField(error_messages={'required': '请确认密码'})

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data

    # 用户名校验
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户名已注册')
        return self.cleaned_data


# 验证失败
def clean_form(form):
    err_dic: dict = form.errors
    err_name = list(err_dic.keys())[0]
    err_msg = err_dic[err_name][0]
    return err_name, err_msg


# 登录
class LoginView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': '',
            'self': None,
        }
        form = LoginForm(request.data, request=request)
        if not form.is_valid():  # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 全部校验完毕 进行登录 操作
        user = form.cleaned_data.get('user')
        auth.login(request, user)
        res['code'], res['msg'] = 0, '登录成功'
        return JsonResponse(res)


# 注册
class SignView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': '',
            'self': None,
        }
        form = SignForm(request.data, request=request)
        if not form.is_valid():  # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 注册成功
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd')
        )
        # 随机绑定头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()

        # 注册后直接登录
        auth.login(request, user)
        res['code'], res['msg'] = 0, '注册成功'
        return JsonResponse(res)
