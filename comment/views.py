from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

# from django.urls import reverse
# from django.shortcuts import render, redirect


def comment_submit(request):
    data = {}
    # refer = request.META.get('HTTP_REFERER')
    form = CommentForm(request.POST, user=request.user)
    content_type = ContentType.objects.get_for_model(Comment).model
    if form.is_valid():
        comment = Comment()
        comment.user = form.cleaned_data['user']
        comment.comment = form.cleaned_data['comment_text']
        comment.content_object = form.cleaned_data['content_object']
        parent = form.cleaned_data['parent']
        # 评论的父级
        if parent:  # 存在父级
            comment.parent = parent
            comment.reply_to = parent.user
            comment.root = parent.root if parent.root else parent  # 评论的根
        comment.save()
        # return redirect(refer, reverse('index'))
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['content_type'] = content_type
        data['comment_time'] = comment.comment_time.astimezone().strftime(
            '%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment
        data['reply_to'] = comment.reply_to.username if parent else ''
        data['root_pk'] = comment.root.pk if comment.root else ''
        data['pk'] = comment.pk
    else:
        # return render(request, 'error.html', {'message': form.errors})
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())[0]
    return JsonResponse(data)
