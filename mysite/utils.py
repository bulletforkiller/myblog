from threading import Thread
from django.conf import settings
from django.core import mail


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
