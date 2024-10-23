from django.core.mail import send_mail

from django_snippets.settings import EMAIL_HOST_USER as sender

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, body, recipient_email):
    send_mail(subject, body, 'tuemail@gmail.com', [recipient_email])

