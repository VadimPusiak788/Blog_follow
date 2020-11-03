from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from account.models import Profile
from .tasks import send_mail_task


@receiver(post_save, sender=Post)
def post_create_send_email(sender, instance, created, **kwargs):
    if created:
        print('sda')

        blog_title = instance.title
        post_url = f'http://0.0.0.0:8000/posts/{instance.pk}'
        user_emails = instance.author.following.values_list(
            'email', flat=True
        )
        for email in user_emails:
            print(email)
            send_mail_task.delay(email, blog_title, post_url)
