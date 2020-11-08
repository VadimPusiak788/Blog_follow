from django.urls import path
from .views import DetailPostView, CreatePost, FollowProfile

app_name = 'blog'

urlpatterns = [
    path('post/', FollowProfile.as_view(), name='post_following'),
    path('post/<int:pk>/', DetailPostView.as_view(), name='post_detail'),
    path('post/create_post/', CreatePost.as_view(), name="create_post")
]
