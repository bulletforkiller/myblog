from django import template
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.simple_tag
def get_comments_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(
        content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comments_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(
        content_type=content_type, object_id=obj.pk,
        parent=None).order_by('-comment_time')


@register.simple_tag
def get_comments_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return CommentForm(
        initial={
            'content_type': content_type.model,
            'object_id': obj.pk,
            'reply_to_id': 0,
        })
