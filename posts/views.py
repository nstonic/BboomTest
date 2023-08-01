from contextlib import suppress

from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer


class UserPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs['user_id'])


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        # ToDo Вывести посты конкретного пользователя
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
