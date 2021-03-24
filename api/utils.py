from django.core.mail import send_mail


def send_confirmation_code(email, code):
    send_mail(
        subject='Yamdb: your confirmation code',
        message='Thank you for registration. '
                f'Your code: {code}',
        from_email='register@yamdb.ru',
        recipient_list=[email],
        fail_silently=False
    )
