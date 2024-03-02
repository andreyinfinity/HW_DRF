from rest_framework import serializers
from lms.models import Course, Lesson
from lms.validators import YouTubeOnlyValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [YouTubeOnlyValidator(field='video_url'),]


class CourseSerializer(serializers.ModelSerializer):
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    num_lessons = serializers.SerializerMethodField()
    subscribe = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_subscribe(self, course):
        return course.subscribe_set.filter(subscriber=course.owner).exists()

    def get_num_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner']
