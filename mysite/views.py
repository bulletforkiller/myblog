import datetime
from django.db.models import Sum
from django.core.cache import cache
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from myblog.models import Blog
from reading_statistics.models import ReadDetail
from reading_statistics.utils import get_recent_views_num


def get_popular(content_type, dates):
    if type(dates) is datetime.date:
        return ReadDetail.objects.filter(date=dates).order_by('-read_nums')[:7]
    elif type(dates) is tuple and len(dates) == 2:
        return Blog.objects.filter(
            read_details__date__lt=dates[0],
            read_details__date__gte=dates[1]).values('id', 'title').annotate(
                read_nums_sum=Sum('read_details__read_nums')).order_by(
                    '-read_nums_sum')[:7]
    else:
        raise ValueError(
            "Arg Dates must be datetime.date or tuple has two elements")


def get_todaly_popular(content_type):
    today = datetime.date.today()
    return get_popular(content_type, today)


def get_yesterday_popular(content_type):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return get_popular(content_type, yesterday)


def get_week_popular(content_type):
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    return get_popular(content_type, (today, seven_days_ago))


def get_month_popular(content_type):
    today = datetime.date.today()
    month_ago = today - datetime.timedelta(days=30)
    return get_popular(content_type, (today, month_ago))


def get_or_create_cache(key_name, func, expire_time=600, **kwargs):
    content_cache = cache.get(key_name)
    if not content_cache:
        content_cache = func(kwargs)
        cache.set(key_name, content_cache, expire_time)
        return content_cache, True
    else:
        return content_cache, False


def home(request):
    blog_content = ContentType.objects.get_for_model(Blog)
    times_list, views_list = get_recent_views_num(blog_content)
    yesterday_populars, _ = get_or_create_cache(
        'yesterday_populars',
        get_yesterday_popular,
        expire_time=7200,
        content_type=blog_content)
    week_populars, _ = get_or_create_cache(
        'week_populars',
        get_week_popular,
        expire_time=3600,
        content_type=blog_content)
    month_populars, _ = get_or_create_cache(
        'month_populars',
        get_month_popular,
        expire_time=3600,
        content_type=blog_content)
    # yesterday_populars = get_yesterday_popular(content_type=blog_content)
    # week_populars = get_week_popular(content_type=blog_content)
    # month_populars = get_month_popular(content_type=blog_content)
    context = {
        'times_list': times_list,
        'views_list': views_list,
        'today_populars': get_todaly_popular(blog_content),
        'yesterday_populars': yesterday_populars,
        'week_populars': week_populars,
        'month_populars': month_populars,
    }
    return render(request, 'index.html', context)
