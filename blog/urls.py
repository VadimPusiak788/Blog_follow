from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import post_following_profiles, DetailPostView, read_post

app_name = 'blog'

urlpatterns = [
    path('post/', post_following_profiles, name='post_following'),
    path('post/<int:pk>/', DetailPostView.as_view(), name='post_detail'),
    path('choise_read/', read_post, name='read_post'),
]