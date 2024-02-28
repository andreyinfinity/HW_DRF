from django.urls import path
from payment import views
from payment.apps import PaymentConfig


app_name = PaymentConfig.name

urlpatterns = [
    path('payments/', views.PaymentList.as_view(), name='payments'),
    path('buy/', views.BuyProduct.as_view(), name='buy'),
    path('success/', views.PaymentStatus.as_view(), name='success'),
]
