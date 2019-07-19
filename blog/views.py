from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog
from .models import BlogType
import markdown
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取页码参数 (Get请求)
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码前后各两页的页码范围
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]

    # 省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # 获取博客分类对应的博客数量
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')

    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)


def blogs_with_type(request, blogs_with_type):
    blog_type = get_object_or_404(BlogType, pk=blogs_with_type)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):  # pk -> primary key

    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)

    # 当前博客
    context['blog'] = blog
    # 当前博客的上一条博客
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 当前博客的下一条博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()

    read_cookie_key = read_statistics_once_read(request, blog)

    blog.content = markdown.markdown(
        blog.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

    response = render_to_response('blog/blog_detail.html', context={'blog': blog})
    response.set_cookie(read_cookie_key, 'true') # 阅读 cookie 标记

    return response
