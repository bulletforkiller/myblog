from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


# Create your models here.
class ReadNum(models.Model):
    read_nums = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<%s 's read_num is %d>" % (self.content_type, self.read_nums)


class ReadDetail(models.Model):
    read_nums = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<%s's read_num is %d>" % (self.content_type, self.read_nums)
