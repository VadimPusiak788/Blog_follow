from django.db import models
from account.models import Profile
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    read = models.ManyToManyField(Profile, related_name='read_post', blank=True)
    total_read = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])