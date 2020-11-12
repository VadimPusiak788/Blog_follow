from django.shortcuts import render, redirect
from account.models import Profile
from itertools import chain
from django.views.generic import DetailView, ListView
from .models import Post
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    context_object_name = 'post_object'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        my_profile = Profile.objects.get(user=self.request.user)
        if my_profile not in post.read.all():
            post.read.add(my_profile)

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        total_views = r.incr(f'post:{post.id}:views')
        context['total_views'] = total_views
        context['read'] = True
        return context


class CreatePost(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    success_url = '/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class FollowProfile(ListView):
    template_name = 'blog/main.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        users = profile.following.all()
        return Post.objects.filter(author__user__in=users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

