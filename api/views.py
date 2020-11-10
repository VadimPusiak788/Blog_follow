from rest_framework import generics
from account.models import Profile
from blog.models import Post
from .serializers import ProfileSerializer, PostSerializers
from django.db.models import Count
from .permissions import IsAuthor


class ProfileAPIView(generics.ListAPIView):
    queryset = Profile.objects.annotate(count_following=Count('following'),
                                        count_post=Count('post'))
    serializer_class = ProfileSerializer


class PostAPIView(generics.ListAPIView):
    permission_classes = (IsAuthor,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthor,)
    queryset = Post.objects.all()
    serializer_class = PostSerializers

