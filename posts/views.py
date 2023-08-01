from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from posts.forms import CreatePostForm
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import CustomUser


class CreatePostView(TemplateView):
    template_name = 'posts/add_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = CreatePostForm()
        return context

    def post(self, *args, **kwargs):
        form = CreatePostForm(self.request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            user_id = self.kwargs['user_id']
            post.user = get_object_or_404(CustomUser, id=user_id)
            post.save()
            return redirect('posts', user_id=user_id)
        return render(self.request, self.template_name, context=form)


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'


class UserPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs['user_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        current_user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        context['current_user'] = current_user
        return context


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
