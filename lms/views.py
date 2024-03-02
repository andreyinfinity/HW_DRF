from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from lms.models import Course, Lesson, Subscribe
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_notification
from payment.services import create_stripe_product, create_stripe_price
from users.permissions import ModeratorPermissionsClass, OwnerPermissionsClass


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        """Метод для добавления пользователя при создании объекта
        и интеграция Stripe"""
        course_name = serializer.validated_data["name"]
        amount = serializer.validated_data["amount"]
        stripe_product = create_stripe_product(course_name)
        stripe_price = create_stripe_price(stripe_product.id, amount)
        serializer.save(
            owner=self.request.user,
            stripe_product=stripe_product.id,
            stripe_price=stripe_price.id,
        )

    def get_queryset(self):
        """
        Метод для отображения всех объектов для модератора
        и только своих объектов для владельца
        """
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Метод для определения прав:
        просмотр и редактирование объекта доступен владельцу и модератору,
        удаление объекта доступно только владельцу,
        создание объекта доступно авторизованному пользователю, но не модератору.
        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, OwnerPermissionsClass | ModeratorPermissionsClass]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, OwnerPermissionsClass]
        else:
            permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]
        return [permission() for permission in permission_classes]


class LessonCreate(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]

    def perform_create(self, serializer):
        """Метод для добавления текущего пользователя в качестве владельца,
        интеграция Stripe"""
        lesson_name = serializer.validated_data["name"]
        amount = serializer.validated_data["amount"]
        stripe_product = create_stripe_product(lesson_name)
        stripe_price = create_stripe_price(stripe_product, amount)
        serializer.save(
            owner=self.request.user,
            stripe_product=stripe_product,
            stripe_price=stripe_price,
        )
        send_notification.delay(serializer.validated_data)


class LessonList(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        """
        Метод для отображения всех объектов для модератора
        и только своих объектов для владельца
        """
        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieve(generics.RetrieveAPIView):
    permission_classes = [OwnerPermissionsClass | ModeratorPermissionsClass]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdate(generics.UpdateAPIView):
    permission_classes = [OwnerPermissionsClass | ModeratorPermissionsClass]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        """Метод для добавления текущего пользователя в качестве владельца"""
        serializer.save(owner=self.request.user)
        send_notification.delay(serializer.data)


class LessonDestroy(generics.DestroyAPIView):
    permission_classes = [OwnerPermissionsClass]
    queryset = Lesson.objects.all()

    def perform_destroy(self, instance):
        send_notification.delay(instance)


class SubscribeAPI(APIView):
    def get(self, *args, **kwargs):
        """Метод для изменения состояния подписки"""
        user = self.request.user
        course = Course.objects.get(pk=kwargs.get('pk'))
        subs_item = Subscribe.objects.filter(subscriber=user, course=course)
        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(subscriber=user, course=course)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
