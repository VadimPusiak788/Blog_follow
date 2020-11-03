from django.urls import path
from .views import DetailPostView, CreatePost, MarkPost, post_following_profiles

app_name = 'blog'

urlpatterns = [
    path('post/', post_following_profiles, name='post_following'),
    path('post/<int:pk>/', DetailPostView.as_view(), name='post_detail'),
    path('choise_read/', MarkPost.as_view(), name='read_post'),
    path('post/create_post/', CreatePost.as_view(), name="create_post")
]