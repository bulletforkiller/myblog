import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics_once(request, obj):
    """
    获取阅读记录，使用cookies来确认是否访问过
    """
    content_type = ContentType.objects.get_for_model(obj)
    cookie_key = '%s__%d_read_yet!' % (content_type.model, obj.pk)

    if not request.COOKIES.get(cookie_key):
        readcount, _ = ReadNum.objects.get_or_create(
            content_type=content_type, object_id=obj.pk)
        readcount.read_nums += 1
        readcount.save()
        date = timezone.now().date()
        read_detail, _ = ReadDetail.objects.get_or_create(
            content_type=content_type, object_id=obj.pk, date=date)
        read_detail.read_nums += 1
        read_detail.save()
    return cookie_key


def get_recent_views_num(content_type):
    today = timezone.now().date()
    time_list = []
    views_list = []
    for i in range(6, -1, -1):
        time = today - datetime.timedelta(days=i)
        time_list.append(time.strftime('%m-%d'))
        read_detail = ReadDetail.objects.filter(
            content_type=content_type, date=time)
        result = read_detail.aggregate(read_nums_sum=Sum('read_nums'))
        views_list.append(result['read_nums_sum'] or 0)
    return time_list, views_list


# class ReadNumExtra():
#     def get_read_num(self):
#         try:
#             content_type = ContentType.objects.get_for_model(self)
#             read_num = ReadNum.objects.get(
#                 content_type=content_type, object_id=self.pk)
#             return read_num.read_nums
#         except exceptions.ObjectDoesNotExist:
#             return 0
