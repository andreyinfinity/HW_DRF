from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение списка пользователей"""


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass
