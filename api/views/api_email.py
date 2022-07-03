from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from django.core.mail import send_mail
import random
from blog import settings
import time
from threading import Thread
from app01.models import UserInfo
from api.models import Email


# 字段校验
class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确的邮箱'})

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserInfo.objects.filter(email=email)
        if user:
            self.add_error('email', '该邮箱已被绑定！')
        return email


# 发送邮箱验证码
class ApiEmail(View):
    def post(self, request):
        res = {
            'self': None,
            'msg': '验证码获取成功！',
            'code': 412,
        }

        form = EmailForm(request.data)

        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 频繁校验
        valid_email_obj = request.session.get('valid_email_obj')
        if valid_email_obj:
            time_stamp = valid_email_obj['time_stamp']
            now_stamp = time.time()
            if (now_stamp - time_stamp) < 60:
                res['msg'] = '请求过于频繁，请稍后再试'
                return JsonResponse(res)
        # 校验成功  设置超时时间
        valid_email_code = ''.join(random.sample('0123456789', 6))
        request.session['valid_email_obj'] = {
            'code': valid_email_code,
            'email': form.cleaned_data['email'],
            'time_stamp': time.time()
        }

        Thread(target=send_mail, args=(
            f'[coderove]:请完善你的信息！',
            f'[coderove]:\n您正在进行的操作为绑定邮箱，邮箱验证码为:{valid_email_code}。\n验证码有效期为5分钟，如非本人操作，请忽略！',
            settings.EMAIL_HOST_USER,
            [form.cleaned_data.get('email')],
            False)).start()
        Email.objects.create(
            email=form.cleaned_data.get('email'),
            content='完善信息'
        )

        res['code'] = 0
        return JsonResponse(res)
