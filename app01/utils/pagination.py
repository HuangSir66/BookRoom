"""
自定义组件,以后想要使用分页组件，需要如下：
在视图函数中：
def pretty_list(request):
    1.根据需求筛选出自己的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')
    2.实例化分页对象
    page_object = Pagination(request,queryset)
    context = {
        'queryset': page_object.page_queryset,#分完页的数据
        'page_string':page_object.html #页码
    }
    return render(request, 'pretty_list.html',context)

在HTML中
    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}
    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
import copy

from django.utils.safestring import mark_safe
class Pagination(object):
    def __init__(self,request,queryset,page_size = 10,page_param='page',plus = 5):
        """....."""
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict.mutable = True
        self.query_dict = query_dict


        page = request.GET.get(page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_param = page_param
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        # 数据总条数
        total_count = queryset.count()
        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus
    def html(self):
        # 计算出当前页的前五页，后五页
        plus = 5
        if self.total_page_count <= 2 * plus + 1:
            # 数据库数据比较少，<11页
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 数据库数据较多，>11页
            # 当页数小于5时
            if self.page <= plus:
                start_page = 1
                end_page = 2 * plus + 1
            else:
                # 当前页大于5#
                # 当前页+5大于总页码
                if self.page + plus > self.total_page_count:
                    start_page = self.total_page_count - 2 * plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - plus
                    end_page = self.page + plus + 1
        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])

        # 首页
        page_str_list.append("<li><a href='?{}'>首页</a></li>".format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param,[self.page - 1])
            prev = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = "<li class = 'active'><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            else:
                ele = "<li><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            self.query_dict.urlencode()
            prev = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(prev)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append("<li><a href='?{}'>尾页</a></li>".format(self.query_dict.urlencode()))

        search_string = """
                        <li>
                            <form style="float:left;margin-left: -1px" method="get">
                                <input name="page"
                                style="position: relative;float:left;display: inline-block;width:80px;border-radius: 0;"
                                type="text" class="form-control" placeholder="页码">
                                <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                            </form>
                        </li>
                        """
        page_str_list.append(search_string)
        page_string = mark_safe(''.join(page_str_list))
        return page_string


