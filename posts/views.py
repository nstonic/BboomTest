from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from posts.forms import CreatePostForm
from posts.models import Post
from users.models import CustomUser


class CreatePostView(TemplateView):
    template_name = 'posts/add_post.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('home')
        return super().get(request, *args, **kwargs)

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
            return redirect('user_posts', user_id=user_id)
        return render(self.request, self.template_name, context={'form': form})


class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        if self.request.user.id == post.user.id:
            user_id = post.user.id
            post.delete()
            return redirect('user_posts', user_id)
        else:
            return redirect('user_posts', self.request.user.id)


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
