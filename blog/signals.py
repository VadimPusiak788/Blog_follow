from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from account.models import Profile

@receiver(post_save, sender=Post)
def post_create_send_email(sender, instance, created, **kwargs):
    if created:
        pass
