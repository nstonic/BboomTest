from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models



class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=64,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
