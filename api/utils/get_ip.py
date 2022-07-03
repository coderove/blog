# 获取ip
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理，获取真实ip
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取ip
    return ip
