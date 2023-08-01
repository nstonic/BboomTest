from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import resolve
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from users.forms import RegisterUserForm, LoginUserForm
from users.models import CustomUser


class UsersView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/users.html'


def register_view(request):
    if request.method == 'GET':
        return redirect('all_users')
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        params = {
            key: request.GET.get(key)
            for key in request.GET
        }
        next_url_name = params.pop('next')
        return redirect(next_url_name, **params)
    context = {
        'errors': form.errors
    }
    return render(request, template_name='errors.html', context=context)


@require_http_methods(['POST'])
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        params = {
            key: request.GET.get(key)
            for key in request.GET
        }
        next_url_name = params.pop('next')
        return redirect(next_url_name, **params)
    else:
        context = {
            'errors': {'login_error': 'Пользователь не найден'}
        }
        return render(request, template_name='errors.html', context=context)


def logout_view(request):
    logout(request)
    params = {
        key: request.GET.get(key)
        for key in request.GET
    }
    next_url_name = params.pop('next')
    return redirect(next_url_name, **params)


def inject_register_form(request):
    current_url = resolve(request.path_info)
    return {
        'register_form': RegisterUserForm(),
        'current_url': current_url.url_name,
        'captured_kwargs': current_url.kwargs
    }


def inject_login_form(request):
    current_url = resolve(request.path_info)
    return {
        'login_form': LoginUserForm(),
        'current_url': current_url.url_name,
        'captured_kwargs': current_url.kwargs
    }
