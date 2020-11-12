from rest_framework import generics
from account.models import Profile
from blog.models import Post
from .serializers import ProfileSerializer, PostSerializers, AllPostProfileSerializers
from django.db.models import Count
from .permissions import IsAuthor


class ProfileAPIView(generics.ListAPIView):
    queryset = Profile.objects.annotate(count_following=Count('following'),
                                        count_post=Count('posts'))
    serializer_class = ProfileSerializer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthor,)

    queryset = Profile.objects.annotate(count_following=Count('following'),
                                        count_post=Count('posts'))
    serializer_class = AllPostProfileSerializers


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.objects.annotate(count_read_post=Count('read'))
    serializer_class = PostSerializers


