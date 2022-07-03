from qiniu import Auth, put_file, put_data

import time
from django.conf import settings

access_key = settings.QINIU_ACCESS_KEY
secret_key = settings.QINIU_SECRET_KEY
bucket_name = settings.QINIU_BUCKET_NAME
qiniu_server = settings.QINIU_SERVER_ADDR
# 鉴权
q = Auth(access_key, secret_key)


def upload_file(path, key=None, prefix='blog/'):
    if not key:
        key = prefix + str(int(time.time())) + '.' + path.split('.')[-1]
    else:
        key = prefix + key + '.' + path.split('.')[-1]
    token = q.upload_token(bucket_name, key, 2)
    put_file(token, key, path, version='v2')
    return qiniu_server + key


def upload_data(file_data, key=None, suffix='.png', prefix='blog/'):
    if not key:
        key = prefix + str(int(time.time())) + suffix
    else:
        key = prefix + key + suffix
    token = q.upload_token(bucket_name, key, 2)
    put_data(token, key, file_data)
    return qiniu_server + key
