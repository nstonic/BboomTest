from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from users.forms import RegisterUserForm, LoginUserForm
from users.models import CustomUser


class UsersView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['users'] = CustomUser.objects.annotate(posts_count=Count('posts'))
        return context


@require_http_methods(['POST'])
def register_view(request):
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        next_url = request.GET.get('next')
        try:
            return redirect(next_url)
        except NoReverseMatch:
            return redirect('home')
    context = {'form': form}
    return render(request, template_name='errors.html', context=context)


@require_http_methods(['POST'])
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        next_url = request.GET.get('next')
        try:
            return redirect(next_url)
        except NoReverseMatch:
            return redirect('home')
    else:
        context = {
            'errors': {'Ошибка авторизации': ['Пользователь не найден']}
        }
        return render(request, template_name='errors.html', context=context)


def logout_view(request):
    logout(request)
    next_url = request.GET.get('next')
    try:
        return redirect(next_url)
    except NoReverseMatch:
        return redirect('home')


def inject_user_form(request):
    return {
        'register_form': RegisterUserForm(),
        'login_form': LoginUserForm(),
        'next': request.path
    }
