from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def profiles_post(self):
        return self.post_set.all()

    def __str__(self):
        return self.user.username
