from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscribe
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import ModeratorPermissionsClass, OwnerPermissionsClass


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update']:
            permission_classes = [OwnerPermissionsClass | ModeratorPermissionsClass]
        elif self.action in ['destroy']:
            permission_classes = [OwnerPermissionsClass]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreate(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonList(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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


class LessonDestroy(generics.DestroyAPIView):
    permission_classes = [OwnerPermissionsClass]
    queryset = Lesson.objects.all()


class SubscribeAPI(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = Course.objects.get(pk=course_id)
        subs_item = Subscribe.objects.filter(subscriber=user, course=course_item)
        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscribe.objects.create(subscriber=user, course=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
