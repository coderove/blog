
from django.http import JsonResponse
from django.shortcuts import redirect


# 装饰器 超级用户  --- 视图函数
def is_super_fun(fun):
    def inner(*args, **kwargs):
        request = args[0]
        if not request.user.is_superuser:
            return redirect('/')
        res = fun(*args, **kwargs)
        return res

    return inner


# 装饰器 超级用户  --- api
def is_super_method(fun):
    def inner(*args, **kwargs):
        request = args[1]
        if not request.user.is_superuser:
            res = {
                'code': 654,
                'msg': '没有进行此操作的权限！'
            }
            return JsonResponse(res)
        res = fun(*args, **kwargs)
        return res

    return inner