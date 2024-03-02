from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from payment.models import Payments
from payment.serializers import PaymentsSerializer
from payment.services import create_stripe_payment


class PaymentList(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date_of_payment']
    filterset_fields = ['method', 'course', 'lesson']


class PaymentCrete(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data["course"]
        lesson = serializer.validated_data["lesson"]
        method = serializer.validated_data["method"]
        if method == "transfer":
            if course:
                stripe_payment = create_stripe_payment(course)
            elif lesson:
                stripe_payment = create_stripe_payment(lesson)
            serializer.save(
                user=user,
                course=course,
                lesson=lesson,
                amount=stripe_payment["amount"],
                stripe_product=stripe_payment["stripe_product"],
                stripe_session_id=stripe_payment["stripe_session_id"],
                stripe_payment_link=stripe_payment["stripe_payment_link"]
            )
        elif method == "cash":
            if course:
                amount = course.price
            elif lesson:
                amount = lesson.price
            serializer.save(
                user=user,
                course=course,
                lesson=lesson,
                amount=amount,
            )
