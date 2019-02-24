from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return 'Profile %s %s' % (self.user.username, self.nickname)


def get_nickname(self):
    if hasattr(self, 'profile'):
        return self.profile.nickname
    else:
        return ''


def has_nickname(self):
    return hasattr(self, 'profile')


def get_nickname_or_username(self):
    return self.profile.nickname if hasattr(self, 'profile') else self.username


# 动态绑定User与自定义的方法
User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username

# User.get_nickname = MethodType(get_nickname, User)
# User.has_nickname = MethodType(has_nickname, User)
# User.get_nickname_or_username = MethodType(get_nickname_or_username, User)
