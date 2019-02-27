from smtplib import SMTPException
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
from mysite.utils import send_mail


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
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['content_type'] = content_type
        data['comment_time'] = comment.comment_time.astimezone().strftime(
            '%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment
        data['reply_to'] = comment.reply_to.username if parent else ''
        data['root_pk'] = comment.root.pk if comment.root else ''
        data['pk'] = comment.pk
        # 同时发送邮件通知
        email = comment.reply_to.email if parent else comment.content_object.author.email
        if email:
            subject = '[lyangly] 您收到一条回复'
            recipient_list = [email]
            message = """<blockquote>尊敬的{0},您的{1}收到一条新的评论，请注意查收。
                        </blockquote>""".format(
                comment.reply_to.username,
                '博客' if not comment.parent else '评论')
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    recipient_list=recipient_list)
            except SMTPException:
                pass
        else:
            print('author does not bind email')
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())[0]
    return JsonResponse(data)
