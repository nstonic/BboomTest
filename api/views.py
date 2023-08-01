from rest_framework import mixins, viewsets

from api.serializers import PostSerializer
from posts.models import Post


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
