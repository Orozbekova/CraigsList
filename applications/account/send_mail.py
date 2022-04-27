
from django.core.mail import send_mail


def send_confirmation_email(code,email):
    full_link = f'http://localhost:8000/account/activate/{code}'

    send_mail(
        'подтвердите свой аккаунт',
        full_link,
        'umutai.orozbekova.ch@gmail.com',
        [email]
    )