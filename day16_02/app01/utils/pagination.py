import math

from django.utils.safestring import mark_safe

from app01 import models


class Pagination(object):

    def __init__(self, request, data_set, page_parma='page', page_size=10, page_show=5):
        page = request.GET.get(page_parma, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page

        self.page_size = page_size
        self.start_page_row = (page - 1) * page_size
        self.end_page_row = page * page_size
        self.data_set = data_set
        self.total_page = math.ceil(data_set.count() / page_size)
        self.page_set = data_set[self.start_page_row: self.end_page_row]



        self.nav_start_page = max(1, page - page_show)
        self.nav_end_page = min(self.total_page, page + page_show)


    def html(self):
        page_str_list = []
        page_str_list.append('<li class="page-item"><a class="page-link" href="?page={}">Previous</a></li>'.format(max(self.page - 1, 1)))

        for i in range(self.nav_start_page, self.nav_end_page + 1):
            if i == self.page:
                ele = '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        page_str_list.append('<li class="page-item"><a class="page-link" href="?page={}">Next</a></li>'.format(
            min(self.page + 1, self.total_page)))

        page_str = mark_safe("".join(page_str_list))
        return page_str




