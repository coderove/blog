## 个人博客系统

环境：python3.9、MySql8、Django 4.0 、vue 2、Element UI。

## 实现功能

### 前端页面

文章：集成MarkDown编辑器、添加文章、编辑文章、展示上一篇和下一篇的链接、文章点赞、文章收藏。

首页：轮播图、精选文章展示、全部文章展示、独家广告位、标签云、网站信息、友链添加、管理员快捷修改文章封面。

心情：可以匿名发布心情，评论心情，删除心情、可预览图片、图片可粘贴上传。

回忆录：发布建站相关的记录，时间轴展示、可单独添加、可单独编辑，可预览图片。

网站导航：添加网站标签、编辑网站标签，可按最新添加、最多收藏、最多点赞进行排序。

文章检索：可按不同字数、不同标签、不同时间及关键字检索全站文章及实现分页器。

登录：可进行登录注册，由后端生成图形验证码。

### 后端页面

管理员页面：Django SimpleUI生成，首页进行了自定义：利用echarts展示七天内用户数据包括

最近注册、最近收藏及邮件发送次数。

个人中心：展示所有收藏的文章、可修改密码、修改头像、可以发送邮箱验证码进行账号和邮箱绑定，利用邮箱登录网站。

管理员：还可以上传头像图片、文章封面，并对所有图片进行展示。



> 页面进行了移动端设备、Ipad、PC设备不同分辨率适配。

### 需要更改的配置

#### 七牛云配置

~~~python
# 七牛云配置
QINIU_ACCESS_KEY = 'xxx'
QINIU_SECRET_KEY = 'xxx'
QINIU_BUCKET_NAME = 'xxx'
QINIU_SERVER_ADDR = 'xxx'
~~~



#### 数据库配置

~~~py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',  # 数据库名
        'USER': 'blog',  # 用户名
        'PASSWORD': '123456',  # 密码
        'HOST': '127.0.0.1',  # 地址
        'PORT': '3306'  # 端口
    }
}
~~~



### 邮箱配置

~~~python
# 配置发送邮件的信息 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.xxx.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'xxx@email.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'xxx'
# 收件人看到的发件人
EMAIL_FROM = 'xxx'
~~~









