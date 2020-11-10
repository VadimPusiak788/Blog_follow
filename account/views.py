from django.shortcuts import redirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
import redis
from django.conf import settings
from blog.models import Post
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class FollowUnfollow(CreateView):
    def post(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=self.request.user)
        pk = self.request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            posts = obj.profiles_post()
            for post in posts:
                post.read = False
                post.save()
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)

        return redirect('account:profiles_list')


class ProfileListView(ListView):
    model = Profile
    template_name = 'account/main.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.all().exclude(user=self.request.user)
        return []


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'account/detail.html'
    context_object_name = 'object_profile'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        total_view = r.incr(f'profile:{view_profile.pk}:views')
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        context['total_view'] = total_view
        return context




