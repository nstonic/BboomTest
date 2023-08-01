from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '********'
            }
        )
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': '********'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'my_username'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'my@email.com'
                }
            )
        }
        labels = {
            'username': '',
            'email': '',
        }


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя пользователя'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Пароль'
                }
            ),
        }
        labels = {
            'username': '',
            'password': ''
        }
