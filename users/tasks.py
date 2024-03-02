from datetime import datetime, timedelta

from celery import shared_task
from django.db.models import Q

from users.models import User


@shared_task
def check_last_login():
    """Функция деактивации неактивного пользователя"""
    month_before = datetime.now() - timedelta(days=30)
    users = User.objects.filter(
        Q(last_login__lte=month_before) |
        Q(last_login=None, date_joined__lte=month_before)
    )
    users.update(is_active=False)
