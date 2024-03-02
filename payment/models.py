from django.db import models
from lms.models import Course, Lesson
from users.models import User


NULLABLE = {'null': True, 'blank': True}
PAYMENT_CHOICES = (
    ('cash', 'наличные'),
    ('transfer', 'перевод на карту'),
)
PAYMENT_STATUS = (
    ('unpaid', 'не оплачено'),
    ('paid', 'оплачено'),
)


class Payments(models.Model):
    """Модель платежей пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_of_payment = models.DateTimeField(auto_now=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name='способ оплаты')
    stripe_product = models.CharField(max_length=500, verbose_name='id продукта Stripe', default='', **NULLABLE)
    stripe_session_id = models.CharField(max_length=500, verbose_name='id сессии оплаты Stripe', default='', **NULLABLE)
    stripe_payment_link = models.URLField(max_length=400, verbose_name="ссылка на оплату Stripe", **NULLABLE)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, verbose_name='статус оплаты', default='unpaid')

    def __str__(self):
        return f'{self.date_of_payment}, {self.user}: {self.course if self.course else self.lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-date_of_payment']
