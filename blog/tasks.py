from django.core.mail import send_mail
from app.celery import app
from django.conf import settings
import smtplib


@app.task
def send_mail_task(email, blog_title, post_url):
    subject = f'New post {blog_title}'
    message = f'Link {post_url}'
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email,
            fail_silently=False
        )
    except smtplib.MTPException as ex:
        print(ex, 'dsf')

