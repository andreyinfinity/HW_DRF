from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from payment.models import Payments
from payment.serializers import PaymentsSerializer


class PaymentList(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_of_payment']
    filterset_fields = ['payment_method', 'paid_course', 'paid_lesson']
