from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from posts.models import Post
from users.models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class PostSerializer(ModelSerializer):
    id = IntegerField(
        required=False,
        read_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body']
