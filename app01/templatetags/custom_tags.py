from django import template
from app01.utils.search import Search
from django.utils.safestring import mark_safe
from app01.models import Tags, Avatars, Menu, Articles

register = template.Library()


# 轮播图

@register.inclusion_tag('custom_tag/headers.html')
def broadcastMap(menu_name, article=None):
    # 文章详情页
    if article:
        cover = article.cover.url.url
        img_list = [cover]
        title = article.title
        slogan_list = [article.abstract[:30]]
        slogan_time = 0
        return locals()

    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    menu_time = menu_obj.menu_time
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    title = menu_obj.title
    slogan_list = menu_obj.abstract.replace('；', ';').replace('\n', ';').split(';')
    slogan_time = menu_obj.abstract_time
    # 不轮播 显示第一章图片
    if not menu_obj.menu_rotation:
        img_list = img_list[0:1]
        menu_time = 0

    if not menu_obj.rotation:
        slogan_list = slogan_list[0:1]
        slogan_time = 0

    return locals()


# 排序
@register.simple_tag
def generate_order_html(request, key):
    # 排序依据
    order = request.GET.get(key, '')
    search_list = []

    if key == 'order':
        search_list.append(('', '综合排序'))
        search_list.append(('-create_date', '最新发布'))
        search_list.append(('-look_count', '最多浏览'))
        search_list.append(('-digg_count', '最多点赞'))
        search_list.append(('-collects_count', '最多收藏'))
        search_list.append(('-comment_count', '最多评论'))

    elif key == 'word':
        order = request.GET.getlist(key, '')
        search_list.append(([''], '全部字数'))
        search_list.append((['0', '100'], '100字以内'))
        search_list.append((['100', '500'], '100-500字'))
        search_list.append((['500', '1000'], '500-1000字'))
        search_list.append((['1000', '3000'], '1000-3000字'))
        search_list.append((['3000', '5000'], '3000-5000字'))
        search_list.append((['5000', '1000000'], '5000字以上'))
    elif key == 'tag':
        search_list.append(('', '全部标签'))
        tag_list = Tags.objects.exclude(articles__isnull=True)
        for tag in tag_list:
            search_list.append((tag.title, tag.title))

    # 获取请求路径
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order_active=order,
        order_list=search_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 个性化展示
# @register.simple_tag
# def generate_advert(advert_list):
#     html_list = []
#     for i in advert_list:
#         if i.img:
#             # 本地上传
#             html_list.append(
#                 f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{i.img.url}" alt=""></a></div>')
#             continue
#         html_list_str = i.img_list
#         html_new_list = html_list_str.replace('；', ';').replace('\n', ';')
#         img_list = html_new_list.split(';')
#         for url in img_list:
#             html_list.append(
#                 f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{url}" alt=""></a></div>')
#
#     return mark_safe(''.join(html_list))


# 心情多张图片显示
@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing_new_list = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing_new_list.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img @error="img_error" src="{i}" alt="">'
    return mark_safe(html_s)


# 回忆录 内容
@register.simple_tag
def generate_history_li(content: str):
    if not content:
        return ''
    content_new_list = content.replace('；', ';').replace('\n', ';')
    content_list = content_new_list.split(';')
    html_s = ''
    for i in content_list:
        html_s += f'<li>{i}</li>'
    return mark_safe(html_s)


# 文章详情页 上一篇和下一篇
@register.simple_tag
def generate_pre_next(article: Articles):
    # 分页 上一篇 下一篇
    article_list = list(Articles.objects.filter(category=article.category))
    now_index = article_list.index(article)
    max_index = len(article_list) - 1
    prev = ''
    next = ''

    if now_index == 0:
        prev = f'<a href="javascript:void (0);">起始之篇</a>'
    else:
        # 上一篇
        prev_article = article_list[article_list.index(article) - 1]
        prev = f'<a href="/article/{prev_article.nid}/">上一篇：{prev_article.title}</a>'

    if now_index == max_index:
        next = f'<a href="javascript:void (0);">终末之篇</a>'
    else:
        # 下一篇
        next_article = article_list[article_list.index(article) + 1]
        next = f'<a href="/article/{next_article.nid}/">下一篇：{next_article.title}</a>'

    return mark_safe(prev + next)


# 计算分类文章数
@register.simple_tag
def calculate_category_count(cid):
    if cid == 0:
        article_query = Articles.objects
        count = article_query.filter(category__isnull=True).count() + article_query.filter(
            category=1).count() + article_query.filter(category=2).count()+ article_query.filter(category=3).count()
        return count

    article_query = Articles.objects.filter(category=cid)
    return article_query.count()
