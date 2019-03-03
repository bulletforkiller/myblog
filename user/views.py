import time
from string import hexdigits
from smtplib import SMTPException
from random import sample, randint
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from mysite.utils import send_mail
from .forms import LoginForm, RegisterForm, ChangeNickForm
from .forms import BindMailForm, ChangePasswordForm, ResetPasswordForm
from .models import Profile


def modal_auth(request):
    data = {}
    if request.is_ajax() and request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            data['status'] = 'SUCCESS'
            return JsonResponse(data)
    data['status'] = 'ERROR'
    return JsonResponse(data)


def auth(request):
    back_on = request.GET.get('from', '')
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect(back_on, reverse('index'))
    else:
        form = LoginForm()
    context = {
        'html_title': '用户登陆',
        'form_title': '用户登陆',
        'form': form,
        'from_link': back_on,
        'submit_text': '登陆',
    }
    return render(request, 'user/auth.html', context)


def register(request):
    back_on = request.GET.get('from', '')
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Remember this
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(back_on, reverse('index'))
    else:
        form = RegisterForm()
    context = {
        'html_title': '用户注册',
        'form_title': '用户注册',
        'form': form,
        'from_link': back_on,
        'send_reason': 'register',
        'submit_text': '注册',
        'need_nav': True,
    }
    return render(request, 'user/send_code.html', context)


def logout_user(request):
    logout(request)
    return redirect(request.GET.get('from', ''), reverse('index'))


# 该模板页面已经进行过用户登陆的测试
def user_detail(request):
    return render(request, 'user/user_detail.html', {})


@login_required(redirect_field_name='from', login_url='/user/login/')
def change_nickname(request):
    back_on = request.GET.get('from', '')
    if request.method == 'POST':
        form = ChangeNickForm(request.POST)
        if form.is_valid():
            new_nickname = form.cleaned_data['new_nickname']
            profile, is_created = Profile.objects.get_or_create(
                user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(back_on, reverse('index'))
    else:
        form = ChangeNickForm()
    context = {
        'html_title': '更改昵称',
        'form_title': '更改昵称',
        'form': form,
        'from_link': back_on,
        'submit_text': '提交更改',
        'need_nav': False,
    }
    return render(request, 'common_form.html', context)


@login_required(redirect_field_name='from', login_url='/user/login/')
def bind_email(request):
    back_on = request.GET.get('from', '')
    if request.method == 'POST':
        form = BindMailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(back_on, reverse('index'))
    else:
        form = BindMailForm()
    context = {
        'html_title': '绑定邮箱',
        'form_title': '绑定邮箱',
        'form': form,
        'from_link': back_on,
        'send_reason': 'bind',
        'submit_text': '绑定',
        'need_nav': False,
    }
    return render(request, 'user/send_code.html', context)


# 该方法只处理 ajax 请求
def send_code(request):
    if request.is_ajax():
        data = {}
        if request.method == 'POST':
            email = request.POST.get('email')
            # 后端限制发送邮件的频率
            last_sent = request.session.get('%s_time' % email, 0)
            forwhat = request.POST.get('forwhat', '')
            if int(time.time()) - last_sent < 60:
                data['status'] = 'ERROR'
                data['message'] = 'Send mail too frequency'
            elif forwhat != 'reset_pass' and User.objects.filter(
                    email=email).exists():
                data['status'] = 'ERROR'
                data['message'] = '邮箱已被绑定'
            else:
                # 生成验证码
                verify_code = ''.join(sample(hexdigits, randint(6, 10)))
                # 存储验证码
                request.session[email] = verify_code
                # 发送验证码
                try:
                    subject = '[lyangly]'
                    recipient_list = [email]
                    if forwhat == 'reset_pass':
                        message = '''<blockquote>您已选择重置本站帐号的密码，
                                    如非本人操作则无需关注本条消息。重置验证码：
                                    %s </blockquote>''' % verify_code
                    else:
                        message = '''<blockquote>尊敬的用户你好，您已在本站绑定该邮箱，
                                    如非本人操作的无需理会本信息。验证码为：
                                    %s </blockquote>''' % verify_code
                    send_mail(
                        subject=subject,
                        message=message,
                        recipient_list=recipient_list)
                except SMTPException:
                    data['status'] = 'ERROR'
                    data['message'] = 'Send mail error'
                else:
                    data['status'] = 'SUCCESS'
                # 存储发送时间
                request.session['%s_time' % email] = int(time.time())
            return JsonResponse(data)
        else:
            return render(request, 'error.html', {'message': '非法的提交'})
    else:
        return render(request, 'error.html', {'message': '非法的提交'})


@login_required(redirect_field_name='from', login_url='/user/login/')
def change_password(request):
    back_on = request.GET.get('from', '')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            # 更改密码需要注销用户并使用户重新登陆
            logout(request)
            return redirect(reverse('index'))
    else:
        form = ChangePasswordForm()
    context = {
        'html_title': '更改密码',
        'form_title': '更改密码',
        'form': form,
        'from_link': back_on,
        'submit_text': '更改',
        'need_nav': False,
    }
    return render(request, 'common_form.html', context)


def reset_password(request):
    back_on = request.GET.get('from', '')
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, request=request)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect(reverse('login'))
    else:
        form = ResetPasswordForm()
    context = {
        'html_title': '更改密码',
        'form_title': '更改密码',
        'form': form,
        'from_link': back_on,
        'send_reason': 'reset_pass',
        'submit_text': '更改',
        'need_nav': False,
    }
    return render(request, 'user/send_code.html', context)
