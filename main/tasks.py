import time

from celery import shared_task
from django.core.mail import send_mail

# @shared_task
from main.celery import app


@app.task(serializers='json')
def send_confirmation_email(code, email):
    full_link = f'http://localhost:8000/account/activate/{code}'

    send_mail(
        'подтвердите свой аккаунт',
        full_link,
        'name.umutai@gmail.com',
        [email]
    )



