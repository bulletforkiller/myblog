from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


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
        return render(request, 'user/auth.html', {'form': form})


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
    return render(request, 'user/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect(request.GET.get('from', ''), reverse('index'))


def user_detail(request):
    return render(request, 'user/user_detail.html', {})
