from django.db import models

from users.models import CustomUser


class Post(models.Model):
    title = models.CharField(
        'Заголовок поста',
        max_length=128
    )
    body = models.TextField('Текст поста')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-id']
