from django.urls import path
from .views import PostAPIView, ProfileAPIView, PostDetail

urlpatterns = [
    path('profile/', ProfileAPIView.as_view()),
    path('post/', PostAPIView.as_view()),
    path('post/<int:pk>/', PostDetail.as_view())
]