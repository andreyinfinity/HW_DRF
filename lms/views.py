from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import ModeratorPermissionsClass, OwnerPermissionsClass


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update']:
            permission_classes = [OwnerPermissionsClass | ModeratorPermissionsClass]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreate(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonList(generics.ListAPIView):
    serializer_class = LessonSerializer

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
