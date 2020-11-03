from django.shortcuts import render, redirect
from account.models import Profile
from itertools import chain
from django.views.generic import DetailView, FormView
from .models import Post
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    context_object_name = 'post_object'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        return post


class MarkPost(CreateView):
    def post(self, request, *args, **kwargs):
        pk = self.request.POST.get('post_pk')
        post = Post.objects.get(pk=pk)
        if not post.read:
            post.read = True
            post.save()
        return redirect('blog:post_following')


class CreatePost(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    success_url = '/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.read = True
        return super().form_valid(form)


def post_following_profiles(request):
    profile = Profile.objects.get(user=request.user)
    user = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in user:
        p = Profile.objects.get(user=u)
        posts_user = p.post_set.all()
        posts.append(posts_user)

    posts.append(profile.post_set.all())
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created)
    return render(request, 'blog/main.html', {'profile': profile, 'posts': qs})
