from django.core.mail import send_mail
from app.celery import app
from django.conf import settings
import smtplib


@app.task
def send_mail_task(email, blog_title, post_url):
    subject = f'New post {blog_title}'
    message = f'Link {post_url}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, email)


