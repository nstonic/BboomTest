from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    @action(methods=['get'], detail=True)
    def posts(self, request, pk: int):
        posts = Post.objects.filter(user__id=pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
