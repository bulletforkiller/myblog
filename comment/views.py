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
        # 表单有效，添加评论
        comment = Comment()
        comment.author = form.cleaned_data['user']
        comment.comment = form.cleaned_data['comment_text']
        comment.content_object = form.cleaned_data['content_object']
        parent = form.cleaned_data['parent']
        if parent:  # 存在父级
            comment.parent = parent
            comment.reply_to = parent.author
            comment.root = parent.root if parent.root else parent  # 评论的根
        comment.save()
        # 评论添加完毕，填写 ajax 的数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.author.get_nickname_or_username()
        data['content_type'] = content_type
        data['comment_time'] = comment.comment_time.astimezone().strftime(
            '%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment
        data['reply_to'] = comment.reply_to.username if parent else ''
        data['root_pk'] = comment.root.pk if comment.root else ''
        data['pk'] = comment.pk
        # 同时发送邮件通知
        main_object = comment.reply_to if parent else comment.author  # 回复的主体
        email = main_object.email
        if email:
            subject = '[lyangly] 您收到一条回复'
            recipient_list = [email]
            message = """<blockquote>尊敬的{0},您的{1}收到一条新的评论，请注意查收。
                        </blockquote>""".format(
                main_object.get_nickname_or_username(),
                '博客' if not comment.parent else '评论')
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    recipient_list=recipient_list)
            except SMTPException:
                pass
        else:
            print('Do not need to send a mail')
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())[0]
    return JsonResponse(data)
