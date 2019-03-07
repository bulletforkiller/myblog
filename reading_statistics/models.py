from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


# Create your models here.
class ReadNum(models.Model):
    read_nums = models.IntegerField(default=0, verbose_name='阅读数')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<%s 's read_num is %d>" % (self.content_type, self.read_nums)


class ReadDetail(models.Model):
    read_nums = models.IntegerField(default=0, verbose_name='阅读统计')
    date = models.DateField(
        default=timezone.now, editable=False, verbose_name='时间')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<%s's read_num is %d>" % (self.content_type, self.read_nums)
