from django.contrib.auth.models import AbstractUser
from django.db import models
from lms.models import Course, Lesson


NULLABLE = {'null': True, 'blank': True}
PAYMENT_CHOICES = (
    ('cash', 'наличные'),
    ('transfer', 'перевод на карту'),
)


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


class Payments(models.Model):
    """Модель платежей пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_of_payment = models.DateField(auto_now=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.date_of_payment}, {self.user}: {self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-date_of_payment']
