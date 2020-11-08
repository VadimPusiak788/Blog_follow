from django.shortcuts import render, redirect
from account.models import Profile
from itertools import chain
from django.views.generic import DetailView
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
        post.read = True
        post.save()
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        total_views = r.incr(f'post:{post.id}:views')
        context['total_views'] = total_views
        return context


class CreatePost(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    success_url = '/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.read = True
        return super().form_valid(form)


class FollowProfile(View):

    @method_decorator(login_required)
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        users = [user for user in profile.following.all()]
        posts = []
        qs = None
        for user in users:
            profile_user = Profile.objects.get(user=user)
            post_user = profile_user.profiles_post()
            posts.append(post_user)

        posts.append(profile.profiles_post())

        if len(posts) > 1:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
        return render(request, 'blog/main.html', {'profile': profile, 'posts': qs})

