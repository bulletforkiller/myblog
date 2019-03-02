from django.conf import settings
from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # 跟踪回复的对象，隐藏的那个表单项
    reply_to_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'reply_to_id'}))
    comment_text = forms.CharField(
        label='评论',
        required=True,
        widget=CKEditorWidget(config_name='comment_ckeditor'),
        error_messages={
            'required': '评论内容不能为空',
        })

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):  # 表单合理性检验
        # 检验用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        # 检验评论的长度是否合理
        if len(self.
               cleaned_data['comment_text']) > settings.MAX_COMMENT_LENGTH:
            raise forms.ValidationError('评论内容过长')
        # 检验评论的对象是否存在
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            content_object = ContentType.objects.get(
                model=content_type).model_class().objects.get(pk=object_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError('被评论的对象不存在')
        else:
            self.cleaned_data['content_object'] = content_object
        finally:
            return self.cleaned_data

    def clean_reply_to_id(self):
        reply_to_id = self.cleaned_data['reply_to_id']
        if not reply_to_id:
            self.cleaned_data['parent'] = None
        elif reply_to_id < 0 or not Comment.objects.filter(
                pk=reply_to_id).exists():
            raise forms.ValidationError('被评论的对象不存在')
        else:
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_to_id)
        return reply_to_id
