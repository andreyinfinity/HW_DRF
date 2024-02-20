from rest_framework import serializers
from lms.models import Course, Lesson
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_num_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'
