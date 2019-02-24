import time
from string import hexdigits
from smtplib import SMTPException
from random import sample, randint
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ChangeNickForm, BindMailForm
from .models import Profile


def auth(request):
    back_on = request.GET.get('from', '')
    is_ajax = request.is_ajax()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            # 处理 ajax
            if is_ajax:
                data = {'status': 'SUCCESS'}
                return JsonResponse(data)
            else:
                return redirect(back_on, reverse('index'))
        else:
            if is_ajax:
                data = {'status': 'ERROR'}
                return JsonResponse(data)
    else:
        form = LoginForm()
        context = {
            'html_title': '用户登陆',
            'form_title': '用户登陆',
            'form': form,
            'from_link': back_on,
            'submit_text': '登陆',
        }
        return render(request, 'common_form.html', context)


def register(request):
    back_on = request.GET.get('from', '')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
            'submit_text': '注册',
        }
    return render(request, 'common_form.html', context)


def logout_user(request):
    logout(request)
    return redirect(request.GET.get('from', ''), reverse('index'))


# 此方法尚未进行测试
@login_required(redirect_field_name='from', login_url='/user/login/')
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
        }
        return render(request, 'common_form.html', context)


@login_required(redirect_field_name='from', login_url='/user/login/')
def bind_email(request):
    back_on = request.GET.get('from', '')
    if request.method == 'POST':
        form = BindMailForm(request.POST)
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
            'submit_text': '绑定',
        }
        return render(request, 'user/bind_mail.html', context)


# 该方法只处理 ajax 请求，并没有其它的可能
@login_required(redirect_field_name='from', login_url='/user/login/')
def send_code(request):
    if request.is_ajax():
        data = {}
        if request.method == 'POST':
            email = request.POST.get('email')
            # 后端限制发送邮件的频率
            last_sent = request.session.get('%s_time' % email, 0)
            if int(time.time()) - last_sent < 60:
                data['status'] = 'ERROR'
                data['message'] = 'Send mail too frequency'
            elif User.objects.filter(email=email).exists():
                data['status'] = 'ERROR'
                data['message'] = '邮箱已被绑定'
            else:
                # 生成验证码
                verify_code = ''.join(sample(hexdigits, randint(6, 10)))
                # 存储验证码
                request.session[email] = verify_code
                # 发送验证码
                try:
                    send_mail(
                        '[lyangly]',
                        '尊敬的用户你好，你已在本站注册。您的验证码是' + verify_code,
                        'killer@lyangly.onmicrosoft.com', [email],
                        fail_silently=False)
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
