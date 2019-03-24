from threading import Thread
from functools import wraps
from django.conf import settings
from django.core import mail
from django.http import HttpResponseServerError
from django_redis import get_redis_connection


def send_mail(subject, message, recipient_list):
    """
    Content is html.
    """
    print('haha')
    t = Thread(
        target=mail.send_mail,
        kwargs={
            'subject': subject,
            'message': '',
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': recipient_list,
            'html_message': message,
            'fail_silently': False,
        })
    t.start()


def interval_time(key_name, expire_time=50):
    """
    Get the object request is limited or not

    Param:
        key_name:       Object query name
        expire_time:    Minimum request interval (milliseconds)

    Return:
        Whether the object is limited or not

    """
    conn = get_redis_connection('default')
    content = conn.get(key_name)
    if not content:
        # ex stands for second, px stands for millisecond
        content = conn.set(key_name, '1', px=expire_time)
        return False
    else:
        return True


def get_client_ip(request):
    """
    Get the client's IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def interval_limit(expired_time=50):
    """
    Limit access frequency by redis, has problems,
    just use nginx to do this.
    This is just a test.

    """

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            pattern = ':1:django:access_limit:ip:{}'
            if interval_time(
                    pattern.format(get_client_ip(request)),
                    expire_time=expired_time):
                return HttpResponseServerError('emmm, error')
            else:
                return view(request, *args, **kwargs)

        return wrapper

    return decorator
