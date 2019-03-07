from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.CharField(max_length=1000, verbose_name='评论内容')
    comment_time = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(
        User,
        related_name='comment',
        on_delete=models.CASCADE,
        verbose_name='作者')
    # 多级评论实现
    parent = models.ForeignKey(
        'self',
        related_name='parent_comment',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='父级评论')
    reply_to = models.ForeignKey(
        User,
        related_name='reply',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='回复给')
    root = models.ForeignKey(
        'self',
        related_name='root_comment',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='回复根')

    def __str__(self):
        # return self.comment
        return '<id: {}, author: {}, content: {}...>'.format(
            self.pk, self.author, self.comment[:10])

    class Meta:
        ordering = ['comment_time']
