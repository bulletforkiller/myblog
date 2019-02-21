from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.CharField(max_length=1000)
    comment_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, related_name='comment', on_delete=models.CASCADE)
    # 多级评论实现
    parent = models.ForeignKey(
        'self',
        related_name='parent_comment',
        null=True,
        on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        User, related_name='reply', null=True, on_delete=models.CASCADE)
    root = models.ForeignKey(
        'self',
        related_name='root_comment',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['comment_time']
