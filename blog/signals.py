from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post
from account.models import Profile
from .tasks import send_mail_task


@receiver(post_save, sender=Post)
def post_create_send_email(sender, instance, created, **kwargs):
    if created:

        blog_title = instance.title
        post_url = f'http://0.0.0.0:8000/posts/{instance.pk}'
        user_emails = instance.author.following.values_list(
            'email', flat=True
        )
        emails = [email for email in user_emails]
        send_mail_task.delay(emails, blog_title, post_url)


@receiver(m2m_changed, sender=Post.read.through)
def read_post_change(sender, instance, **kwargs):
    instance.total_read = instance.read.count()
    instance.save()