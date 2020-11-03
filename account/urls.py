from django.urls import path
from .views import ProfileListView, ProfileDetailView, FollowUnfollow

app_name = 'account'

urlpatterns = [
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('switch_follow/', FollowUnfollow.as_view(), name='follow_unfollow'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='detail_profile')
]