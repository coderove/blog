import base64

from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover, avatar_delete, cover_delete, UserInfo
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from api.utils.api_qiniu import upload_data
from api.utils.power_control import is_super_method


class AvatarView(View):
    @is_super_method
    def post(self, request):
        res = {
            'code': 552,
            'msg': '文件上传失败'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)

        file: InMemoryUploadedFile = request.FILES.get('file')
        # 文件校验

        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            res['msg'] = '文件上传失败:类型应为png或者jpg图片'
            return JsonResponse(res)

        size_kb = file.size / 1024 / 1024
        if size_kb > 2:
            res['msg'] = '文件上传失败:大小应小于2MB'
            return JsonResponse(res)

        Avatars.objects.create(url=file)
        res['code'] = 0
        res['msg'] = '文件上传成功'
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'code': 564,
            'msg': '头像删除成功'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)
        avatar_query = Avatars.objects.filter(nid=nid)

        if not avatar_query:
            res['msg'] = '图片已被删除'
            return JsonResponse(res)

        # 第三方注册，查看是否有人使用
        obj: Avatars = avatar_query.first()
        user_query = UserInfo.objects.filter(Q(sign_status=1) | Q(sign_status=2))
        for user in user_query:
            if obj.url.url == user.avatar_url:
                res['msg'] = '该图片正在被使用，无法删除！'
                return JsonResponse(res)

        avatar_delete(obj)
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 文章封面
class CoverView(View):
    @is_super_method
    def post(self, request):
        res = {
            'code': 552,
            'msg': '文件上传失败'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)

        file: InMemoryUploadedFile = request.FILES.get('file')
        # 文件校验

        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            res['msg'] = '文件上传失败:类型应为png或者jpg图片'
            return JsonResponse(res)

        size_kb = file.size / 1024 / 1024
        if size_kb > 2:
            res['msg'] = '文件上传失败:大小应小于2MB'
            return JsonResponse(res)

        Cover.objects.create(url=file)
        res['code'] = 0
        res['msg'] = '文件上传成功'
        return JsonResponse(res)

    @is_super_method
    def delete(self, request, nid):
        res = {
            'code': 564,
            'msg': '封面删除成功'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败，仅管理员可删除'
            return JsonResponse(res)
        cover_query = Cover.objects.filter(nid=nid)
        if not cover_query:
            res['msg'] = '图片已被删除'
            return JsonResponse(res)
        cover_delete(cover_query.first())
        cover_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 回忆录 粘贴上传
class PasteUpload(View):
    def post(self, request):
        img = request.data.get('image')
        ines = img.split('base64,')
        imgData = base64.b64decode(ines[1])
        url = upload_data(imgData)
        return JsonResponse({'url': url})


# editor 图片上传
class EditorPasteUpload(View):
    def post(self, request):
        res = {
            'msg': '成功',
            'success': 1,
            'code': 200,
        }
        data = request.data
        print(data)
        return JsonResponse(res)
