from django.views.generic import ListView

from users.forms import RegisterUserForm, LoginUserForm
from users.models import CustomUser


class UsersView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/users.html'


def inject_register_form(request):
    return {'register_form': RegisterUserForm()}


def inject_login_form(request):
    return {'login_form': LoginUserForm()}
