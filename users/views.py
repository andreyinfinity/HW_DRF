from rest_framework import generics
from users.models import User
from users.serializers import UserRegisterSerializer, UserSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
