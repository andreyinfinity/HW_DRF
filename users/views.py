from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.permissions import OwnerPermissionsClass, IsSelf
from users.serializers import UserSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsSelf]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdate(generics.UpdateAPIView):
    permission_classes = [IsSelf]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserDelete(generics.DestroyAPIView):
    permission_classes = [IsSelf]
    queryset = User.objects.all()
