from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(email='test@test.ru', password='test')
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        # Создание курса
        self.client.post(path=reverse('lms:course-list'), data={"name": "test_course"})

        self.create_url = reverse('lms:lesson-create')
        self.data = {
            "name": "Test lesson",
            "description": "Test description",
            "video_url": "https://www.youtube.com/watch?v=v6GHc_uabM0",
            "course": 1
        }

    def test_create_lesson(self):
        response = self.client.post(path=self.create_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
