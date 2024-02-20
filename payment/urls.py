from django.urls import path
from payment import views
from payment.apps import PaymentConfig


app_name = PaymentConfig.name

urlpatterns = [
    path('payments/', views.PaymentList.as_view(), name='payments'),

]
