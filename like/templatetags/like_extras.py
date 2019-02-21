from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ThumbAll, ThumbUp

register = template.Library()


@register.simple_tag
def get_likes_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.pk
    thumb_all, is_created = ThumbAll.objects.get_or_create(
        content_type=content_type, object_id=object_id)
    return thumb_all.likes_count


@register.simple_tag(takes_context=True)
def get_likes_states(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    else:
        return 'active' if ThumbUp.objects.filter(
            content_type=content_type, object_id=obj.pk,
            user=user).exists() else ''


@register.simple_tag
def get_content_type(obj):
    return ContentType.objects.get_for_model(obj).model
