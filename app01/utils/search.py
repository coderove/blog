from urllib.parse import urlencode


# 搜索操作
class Search:
    def __init__(self, key, order_active, order_list, query_params):
        """
        :param key:搜索模式
        :param order_active: 当前选中的状态
        :param order_list: 请求的字段列表
        :param query_params: 请求路径
        """
        self.order_list = order_list
        self.key = key
        self.order_active = order_active
        self.query_params = {}

        for i in query_params:
            self.query_params[i] = query_params.getlist(i)

    def order_html(self):
        order_list = []
        for li in self.order_list:
            self.query_params[self.key] = li[0]
            if self.order_active == li[0] or [self.order_active] == li[0]:
                li = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
            else:
                li = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_list.append(li)
        return ''.join(order_list)

    @property
    def query_encode(self):
        # self.query_params.urlencode()
        return urlencode(self.query_params, doseq=True)

# if __name__ == '__main__':
#     order = Search(
#         order_list=[
#             ('-change_date', '综合排序'),
#             ('creat_date', '最新发布'),
#             ('-look_count', '最多浏览'),
#             ('-digg_count', '最多点赞'),
#             ('-collects_count', '最多收藏'),
#             ('-comment_count', '最多评论')
#         ],
#         query_params={'key': 'c'}
#     )
