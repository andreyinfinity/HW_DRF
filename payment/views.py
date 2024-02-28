from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import Payments
from payment.serializers import PaymentsSerializer
from payment.services import create_payment, check_payment_status


class PaymentList(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_of_payment']
    filterset_fields = ['payment_method', 'paid_course', 'paid_lesson']


class BuyProduct(APIView):
    def post(self, request, *args, **kwargs):
        """Запрос на покупку продукта. Передается тип продукта (course или lesson) и его id"""
        data = {
            'product_type': request.data.get('product_type'),
            'product_id': request.data.get('product_id'),
            'user_id': request.user.pk
        }

        return Response(create_payment(data))


class PaymentStatus(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'product_type': request.data.get('product_type'),
            'product_id': request.data.get('product_id'),
            'user_id': request.user.pk
        }
        return Response(check_payment_status(data))
