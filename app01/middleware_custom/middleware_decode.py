from django.utils.deprecation import MiddlewareMixin
import json
from api.utils.get_ip import get_ip
from django.core.cache import cache

# 解析post请求
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data_dict = json.loads(request.body)
            request.data = data_dict

    # 响应
    def process_response(self, request, response):
        return response


# 统计网站在线人数
class Statistical(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        ip = get_ip(request)
        online_ips = list(cache.get('online_ips', []))

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        cache.set(ip, 0, 10)  # 超时时间 1s

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set('online_ips', online_ips)  # 存入cache

        request.online_list = online_ips
