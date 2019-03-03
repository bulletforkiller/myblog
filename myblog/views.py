from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render
from .models import Blog, BlogType
from reading_statistics.utils import read_statistics_once

# Create your views here.


def get_blog_list_common(request, blogs):
    # 得到博客的所有类型，用于生成类型边栏
    blog_types = BlogType.objects.all()
    # 分页机制的实现
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs, settings.BLOGS_NUM_PER_PAGE)
    blog_page = paginator.get_page(page_num)
    current_page_num = blog_page.number
    page_range = [
        x for x in range(
            max(current_page_num - 2, 1),
            min(current_page_num + 2, paginator.num_pages) + 1)
    ]
    # 加上省略标记
    if page_range[0] > 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('...')
    # 添加首页和尾夜
    if 1 not in page_range:
        page_range.insert(0, 1)
    if paginator.num_pages not in page_range:
        page_range.append(paginator.num_pages)
    # 用于返回的内容
    return {
        'blog_types': blog_types,
        'page_of_blogs': blog_page,
        'page_range': page_range,
        # 生成日期分类边栏
        'blog_dates': Blog.objects.dates('create_time', 'month', order='DESC')
    }


@cache_page(60 * 5)
def blog_list(request):
    blogs = Blog.objects.all()  # 使用 get_list_or_404 没有博客时返回404,无法显示
    return render(request, 'myblog/blog_list.html',
                  get_blog_list_common(request, blogs))


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    cookie_key = read_statistics_once(request, blog)
    previos_blog = Blog.objects.filter(create_time__gt=blog.create_time).last()
    next_blog = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context = {
        'user': request.user,
        'blog': blog,
        'previous_blog': previos_blog,
        'next_blog': next_blog,
    }
    response = render(request, 'myblog/blog_detail.html', context)
    response.set_cookie(cookie_key, 'true')
    return response


@cache_page(60 * 5)
def blogs_with_type(request, blogs_with_type):
    blog_type = get_object_or_404(BlogType, pk=blogs_with_type)
    blogs = Blog.objects.filter(blog_type__pk=blog_type.pk)
    context = {
        'blog_this_type': blog_type,
    }
    context.update(get_blog_list_common(request, blogs))
    return render(request, 'myblog/blog_with_type.html', context)


@cache_page(60 * 5)
def blogs_by_date(request, year, month):
    blogs = Blog.objects.filter(
        create_time__year=year, create_time__month=month)
    context = {
        'blog_this_date': '%d年%d月' % (year, month),
    }
    context.update(get_blog_list_common(request, blogs))
    return render(request, 'myblog/blog_by_date.html', context)
