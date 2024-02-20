from django.contrib import admin

from payment.models import Payments


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass
