from rest_framework import serializers
from payment.models import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
        read_only_fields = ['user', 'amount', 'stripe_product', 'stripe_session_id', 'stripe_payment_link', 'status']
