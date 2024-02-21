from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.permissions import OwnerPermissionsClass
from users.serializers import UserSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_user = serializer.save()
        password = serializer.data.get("password")
        new_user.set_password(password)
        new_user.save()


class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnerPermissionsClass]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdate(generics.UpdateAPIView):
    permission_classes = [OwnerPermissionsClass]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save()
        password = serializer.data.get("password")
        user.set_password(password)
        user.save()


class UserDelete(generics.DestroyAPIView):
    permission_classes = [OwnerPermissionsClass]
    queryset = User.objects.all()
