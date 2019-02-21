from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import ThumbAll, ThumbUp


def success_response(likes_num):
    data = {
        'status': 'SUCCESS',
        'likes_num': likes_num,
    }
    return JsonResponse(data)


def error_response(code, message):
    data = {
        'status': 'ERROR',
        'code': code,
        'message': message,
    }
    return JsonResponse(data)


# Create your views here.
def like_state_change(request):
    # 用户身份鉴别
    user = request.user
    if not user.is_authenticated:
        return error_response(401, 'User is not authenticated')
    # 获取相关数据
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
    except ObjectDoesNotExist:
        return error_response(404, 'object does not exist')
    # 获取该用户的点赞记录
    had_thumbed = ThumbUp.objects.filter(
        content_type=content_type, object_id=object_id, user=user).exists()
    # 获取或创建该对象的点赞总数统计
    thumb_all, is_created = ThumbAll.objects.get_or_create(
        content_type=content_type, object_id=object_id)
    # 判断用户的行为
    if request.GET.get('is_like') == 'true':
        if had_thumbed:
            return error_response(403, 'Already liked')
        else:
            thumb_up = ThumbUp.objects.create(
                content_type=content_type, object_id=object_id, user=user)
            # thumb_up.save()
            thumb_all.likes_count += 1
            thumb_all.save()
            return success_response(thumb_all.likes_count)
    else:  # 取消点赞
        if not had_thumbed:
            return error_response(403, "had not liked this")
        else:
            thumb_up = ThumbUp.objects.get(
                content_type=content_type, object_id=object_id, user=user)
            thumb_up.delete()
            thumb_all.likes_count -= 1
            thumb_all.save()
            return success_response(thumb_all.likes_count)
