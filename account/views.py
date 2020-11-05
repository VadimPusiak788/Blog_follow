from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile


class FollowUnfollow(CreateView):
    def post(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=self.request.user)
        pk = self.request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)

        return redirect('account:profiles_list')


class ProfileListView(ListView):
    model = Profile
    template_name = 'account/main.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        # if self.request.is_authenticated:
        #     return []
        return Profile.objects.all().exclude(user=self.request.user)


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
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        return context




