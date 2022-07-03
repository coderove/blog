# from urllib.parse import urlencode
# import math
#
#
# class PageInation():
#     def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11,
#                  position='anchor_point'):
#         """
#         :param current_page:当前页码
#         :param all_count: 数据库总条数
#         :param pager_page_count:最多显示多少个页码
#         :param per_page:一页展示多少条
#
#         :param base_url:原始url
#         :param query_params:保留原搜索条件
#         :param position:index刷新的锚点
#         """
#
#         self.all_count = all_count
#         self.base_url = base_url
#         self.query_params = query_params
#         self.per_page = per_page
#         self.pager_page_count = pager_page_count
#         self.position = position
#         # 计算一共有多少个页码
#         self.current_count = math.ceil(all_count / per_page)
#         # 1.满足条件的数字
#         try:
#             self.current_page = int(current_page)
#             if not (0 < self.current_page <= self.current_count):
#                 self.current_page = 1
#         except Exception:
#             self.current_page = 1
#
#         # 计算页码中值
#         self.half_page_count = int(self.pager_page_count / 2)
#         if self.current_count < self.pager_page_count:
#             # 可分页码小于最大显示页码，以最大显示页码为主
#             self.pager_page_count = self.current_page
#
#     # 计算起始值和终值
#     def page_html(self):
#         # 1.正常情况下
#         # 20 9       4 5 6 7 8 9 10 11 12 13 14
#         start = self.current_page - self.half_page_count
#         end = self.current_page + self.half_page_count
#
#         if self.current_page <= self.half_page_count:
#             start = 1
#             end = self.pager_page_count
#
#         if self.current_page + self.half_page_count >= self.current_count:
#             start = self.current_count - self.pager_page_count
#             end = self.current_count
#
#         # 生成分页  <li><a href=""></a></li>
#         page_list = []
#
#         # 上一页
#         if self.current_page != 1:
#             self.query_params['page'] = self.current_page - 1
#             page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">上一页</a></li>')
#
#         # 数字部分
#         for i in range(start, end + 1):
#             self.query_params['page'] = i
#             if self.current_page == i:
#                 li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
#             else:
#                 li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
#             page_list.append(li)
#
#         # 下一页
#         if self.current_page != self.current_count:
#             self.query_params['page'] = self.current_page + 1
#             page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">下一页</a></li>')
#
#         return ''.join(page_list)
#
#     @property
#     def query_encode(self):
#         # self.query_params.urlencode()
#         return urlencode(self.query_params)
#
#     @property
#     def start(self):
#         return (self.current_page - 1) * self.per_page
#
#     @property
#     def end(self):
#         return self.current_page * self.per_page
#
#
# if __name__ == '__main__':
#     page = PageInation(
#         current_page=1,
#         all_count=6,
#         base_url='article/',
#         query_params={'tag': 'python'},
#         per_page=1,
#         pager_page_count=7
#     )
#     print(page.page_html())
