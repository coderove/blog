import datetime
import pendulum
from app01.models import Avatars, Cover, Advert
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# 自定义过滤器

# 用户是否收藏文章
@register.filter
def is_user_collects(article, request):
    # 未登录
    if str(request.user) == 'AnonymousUser':
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''


# 是否有搜索内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'


# 时间格式化
@register.filter
def date_format(date: datetime.datetime):
    pendulum.set_locale('zh')
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference


# 头像使用计数
@register.filter
def calculate_to_avatar_count(avatar: Avatars):
    count = avatar.moodcomment_set.count() + avatar.moods_set.count() + avatar.userinfo_set.count()
    if count:
        return ''
    else:
        return 'no_avatar'


# 文章使用计数
@register.filter
def calculate_to_cover_count(cover: Cover):
    count = cover.articles_set.count()
    if count:
        return ''
    else:
        return 'no_cover'


# 获取标签
@register.filter
def get_tags(tag_list):
    return mark_safe(''.join([f'<i>{i.title}</i>' for i in tag_list]))


# 获取所有的nid -收藏的文章
@register.filter
def get_coll_nid(lis):
    return [i.nid for i in lis]


# 生成轮播的图片 -- 原广告位的位置
@register.filter
def generate_advert(advert_list):
    lis = []
    for i in advert_list:
        item = {}
        if i.img:  # 用户上传
            item['url'] = i.img.url
            item['title'] = i.title
            item['href'] = i.href
            lis.append(item)
        else:
            html_list_str = i.img_list
            html_new_list = html_list_str.replace('；', ';').replace('\n', ';')
            img_list = html_new_list.split(';')
            for u in img_list:
                item['url'] = u
                item['title'] = i.title
                item['href'] = i.href
                lis.append(item)

    return lis
