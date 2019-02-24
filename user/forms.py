from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        min_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名',
        }),
        required=True,
        error_messages={
            'max_length': '用户名过长',
            'min_length': '用户名过短',
            'required': '用户名不能为空',
            'invalid:': '错误的格式',
        })
    password = forms.CharField(
        label='密码',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码',
        }),
        required=True,
        error_messages={
            'min_length': '密码至少为8位',
            'required': '密码不能为空',
        })

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=5,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名',
        }),
        required=True,
        error_messages={
            'max_length': '用户名过长',
            'min_length': '用户名过短',
            'required': '用户名不能为空',
            'invalid:': '错误的用户名格式',
        })
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱',
        }),
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid:': '错误的邮箱格式',
        })
    password = forms.CharField(
        label='密码',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码',
        }),
        required=True,
        error_messages={
            'min_length': '过短的密码',
            'required': '密码不能为空',
            'invalid:': '错误的密码格式',
        })
    password_again = forms.CharField(
        label='密码确认',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请再次输入密码',
        }),
        required=True,
        error_messages={
            'min_length': '过短的密码',
            'required': '密码不能为空',
            'invalid:': '错误的密码格式',
        })

    def clean_username(self):
        username = self.cleaned_data['username']
        # 对用户名的过滤待定
        if User.objects.filter(username=username).exists():
            print(username)
            raise forms.ValidationError('用户名已经存在')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print(email)
            print(User.objects.filter(email=email))
            raise forms.ValidationError('E-mail已被注册')
        else:
            return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次密码不同')
        else:
            return password_again


class ChangeNickForm(forms.Form):
    # 后端是否需要验证待定
    new_nickname = forms.CharField(
        label='新昵称',
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入新的昵称',
        }),
        error_messages={
            'required': '新昵称不能为空',
            'max_length': '昵称最长限20个字符',
        })


class BindMailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入有效的邮箱'
        }),
        error_messages={
            'invalid': '非法的邮箱格式',
            'required': '邮箱不能为空',
        })
    verify_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入验证码'
        }))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_verify_code(self):
        email = self.cleaned_data['email']
        verify_code = self.cleaned_data['verify_code'].strip()
        raw_code = self.request.session.get(email, '')
        if not verify_code:
            raise forms.ValidationError('验证码不能为空')
        elif raw_code != verify_code:
            raise forms.ValidationError('错误的验证码')
        else:
            del self.request.session[email]
            return verify_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入旧密码',
        }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少为8位'
        })

    new_password = forms.CharField(
        label='新密码',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入新密码',
        }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少为8位'
        })

    new_password_again = forms.CharField(
        label='新密码确认',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请再次输入新密码',
        }),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少为8位'
        })

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        password = self.cleaned_data['old_password']
        if self.user.check_password(password):
            return password
        else:
            raise forms.ValidationError('旧密码错误')

    def clean(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_passord_again']
        if new_password != new_password_again or not new_password:
            raise forms.ValidationError('新密码不匹配')
        else:
            return new_password
