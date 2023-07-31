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
    user: User = None

    def get_user(self):
        with suppress(KeyError, User.DoesNotExist, User.MultipleObjectsReturned):  # noqa
            user_id = self.kwargs['user']
            self.user = User.objects.get(user_id=user_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['user'] = self.user

    def get_queryset(self):
        return Post.objects.filter(user_id=self.user.id)

    def get(self, request, *args, **kwargs):
        self.get_user()
        if not self.user:
            return HttpResponseBadRequest
        else:
            return super().get(request, *args, **kwargs)


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
