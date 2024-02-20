from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_payment_history(self, user):
        return [str(payment) for payment in user.payments_set.filter(user=user)]

    def create(self, validated_data):
        """Шифрование пароля при регистрации"""
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, user, validated_data):
        """Шифрование пароля при обновлении профиля"""
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'
