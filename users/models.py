from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


def user_directory_path(instance, filename):
    """Функция для формирования директории user_<id>/<filename>"""
    return "user_{0}/{1}".format(instance.id, filename)


class User(AbstractUser):
    """Пользователь"""
    username = None
    image = models.ImageField(upload_to=user_directory_path, verbose_name='аватар', **NULLABLE)
    email = models.EmailField(verbose_name='e-mail', unique=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} ({self.first_name})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
