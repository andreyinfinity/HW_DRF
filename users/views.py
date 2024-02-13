from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from users.models import User, Payments
from users.serializers import UserRegisterSerializer, UserSerializer, PaymentsSerializer
from rest_framework.filters import OrderingFilter


class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentList(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_of_payment']
    filterset_fields = ['payment_method', 'paid_course', 'paid_lesson']
