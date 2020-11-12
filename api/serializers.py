from rest_framework import serializers
from account.models import Profile
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfilePost(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = ('user', )


class ProfileSerializer(serializers.ModelSerializer):
    count_following = serializers.IntegerField()
    user = UserSerializers()
    count_post = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('user', 'count_following', 'count_post')


class PostSerializers(serializers.ModelSerializer):
    author = ProfilePost(required=True)

    class Meta:
        model = Post
        fields = ('pk', 'title', 'body', 'author', 'total_read')


class AllPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'created', 'total_read')


class AllPostProfileSerializers(serializers.ModelSerializer):
    posts = AllPostSerializers(many=True)
    count_following = serializers.IntegerField()
    user = UserSerializers()
    count_post = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ('user', 'count_post', 'count_following', 'posts')
