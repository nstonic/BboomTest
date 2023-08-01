from rest_framework import mixins, viewsets

from api.serializers import PostSerializer, UserSerializer
from posts.models import Post
from users.models import CustomUser


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class UserViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
