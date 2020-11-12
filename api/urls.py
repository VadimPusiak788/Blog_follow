from django.urls import path
from .views import PostAPIView, ProfileAPIView, PostDetailAPI,\
    ProfileDetailAPIView

urlpatterns = [
    path('profile/', ProfileAPIView.as_view()),
    path('post/', PostAPIView.as_view()),
    path('post/<int:pk>/', PostDetailAPI.as_view()),
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view())
]