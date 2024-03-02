from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from lms.models import Lesson, Course, Subscribe
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование CRUD уроков"""
    def setUp(self):
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(email='test@test.ru', password='test')
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        # Создание тестового курса
        self.course = Course.objects.create(name="test_course", owner=self.user)

    def test_create_lesson(self):
        """Тест создания урока и проверка валидации поля video_url"""
        # Эндпойнт создания урока
        url = reverse('lms:lesson-create')
        # Невалидные тестовые данные со сторонней ссылкой video_url
        data = {
            "name": "Test lesson",
            "description": "Test description",
            "video_url": "https://my.sky.pro/student-cabinet/stream-lesson/85086/theory/7",
            "course": self.course.pk
        }

        response = self.client.post(path=url, data=data)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка ответа с ошибкой валидации
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Можно добавлять ссылки только с Youtube']}
        )
        # Проверка, что запись не создалась в БД
        self.assertFalse(Lesson.objects.all().exists())

        # Валидные тестовые данные
        data = {
            "name": "Test lesson",
            "description": "Test description",
            "video_url": "https://www.youtube.com/watch?v=v6GHc_uabM0",
            "course": self.course.pk
        }

        response = self.client.post(path=url, data=data)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {
                'id': 1,
                'name': 'Test lesson',
                'description': 'Test description',
                'picture': None,
                'video_url': 'https://www.youtube.com/watch?v=v6GHc_uabM0',
                'course': self.course.pk,
                'owner': self.user.pk
            }
        )
        # Проверка созданной записи в БД
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_view_lessons(self):
        """Тест просмотра списка уроков"""
        # Создание тестовых уроков
        lesson1 = Lesson.objects.create(name="Test list view lesson 1", course=self.course, owner=self.user)
        lesson2 = Lesson.objects.create(name="Test list view lesson 2", course=self.course, owner=self.user)
        # Эндпоинт для просмотра списков уроков
        url = reverse('lms:lessons')

        response = self.client.get(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {
                'count': 2,
                'next': None,
                'previous': None,
                'results':
                    [{
                        'id': lesson1.pk,
                        'name': 'Test list view lesson 1',
                        'description': None,
                        'picture': None,
                        'video_url': None,
                        'course': self.course.pk,
                        'owner': self.user.pk
                    },
                    {
                        'id': lesson2.pk,
                        'name': 'Test list view lesson 2',
                        'description': None,
                        'picture': None,
                        'video_url': None,
                        'course': self.course.pk,
                        'owner': self.user.pk
                    }]
                })
        # Проверка количества записей в БД
        self.assertEqual(Lesson.objects.filter(owner=self.user).count(), 2)

    def test_retrieve_view_lesson(self):
        """Тест детального просмотра урока"""
        lesson = Lesson.objects.create(name="Test retrieve view lesson", course=self.course, owner=self.user)
        # Эндпоинт для просмотра урока
        url = reverse('lms:lesson-retrieve', args=[lesson.pk])

        response = self.client.get(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {
                        'id': lesson.pk,
                        'name': 'Test retrieve view lesson',
                        'description': None,
                        'picture': None,
                        'video_url': None,
                        'course': self.course.pk,
                        'owner': self.user.pk
            })

    def test_update_lesson(self):
        """Тест редактирования урока"""
        lesson = Lesson.objects.create(name="Test update lesson", course=self.course, owner=self.user)
        # Эндпоинт для редактирования урока
        url = reverse('lms:lesson-update', args=[lesson.pk])

        response = self.client.patch(path=url, data={"name": "Test update lesson success"})
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {
                        'id': lesson.pk,
                        'name': 'Test update lesson success',
                        'description': None,
                        'picture': None,
                        'video_url': None,
                        'course': self.course.pk,
                        'owner': self.user.pk
            })

        response = self.client.put(path=url, data={"name": "Test update lesson using PUT", "course": self.course.pk})
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {
                        'id': lesson.pk,
                        'name': 'Test update lesson using PUT',
                        'description': None,
                        'picture': None,
                        'video_url': None,
                        'course': self.course.pk,
                        'owner': self.user.pk
            })

    def test_delete_lesson(self):
        """Тест удаления урока"""
        lesson = Lesson.objects.create(name="Test delete lesson", course=self.course, owner=self.user)
        # Эндпоинт для удаления урока
        url = reverse('lms:lesson-delete', args=[lesson.pk])
        # Проверка наличия объекта в БД
        self.assertTrue(Lesson.objects.all().exists())

        response = self.client.delete(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка отсутствия объекта в БД
        self.assertFalse(Lesson.objects.all().exists())


class SubscribeTestCase(APITestCase):
    """Тестирование подписки"""
    def setUp(self):
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(email='test@test.ru', password='test')
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        """Тест подписки/отписки пользователя на курс"""
        # Создание тестового курса
        course = Course.objects.create(name="test_course", owner=self.user)
        # Эндпоинт для подписки/отписки
        url = reverse('lms:subscribe', args=[course.pk])

        response = self.client.post(path=url)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})
        # Проверка появления записи в БД о подписке
        self.assertTrue(Subscribe.objects.all().exists())

        response = self.client.post(path=url)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})
        # Проверка отсутствия записи в БД о подписке
        self.assertFalse(Subscribe.objects.all().exists())


class CourseTestCase(APITestCase):
    """Тестирование CRUD курса"""
    def setUp(self):
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(email='test@test.ru', password='test')
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тест создания курса пользователем"""
        # Эндпоинт создания курса
        url = reverse('lms:course-list')
        # Тестовые данные для создания курса
        data = {"name": "Test course create"}
        response = self.client.post(path=url, data=data)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {'description': None,
                    'id': 1,
                    'lessons': [],
                    'name': 'Test course create',
                    'num_lessons': 0,
                    'owner': self.user.pk,
                    'picture': None,
                    'subscribe': False})
        self.assertTrue(Course.objects.all().exists())

    def test_list_view_courses(self):
        """Тест отображения списка курсов пользователя"""
        # Эндпоинт списка курсов
        url = reverse('lms:course-list')
        course1 = Course.objects.create(name="test list 1", owner=self.user)
        course2 = Course.objects.create(name="test list 2", owner=self.user)

        response = self.client.get(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results': [
                 {
                    'description': None,
                    'id': course1.pk,
                    'lessons': [],
                    'name': 'test list 1',
                    'num_lessons': 0,
                    'owner': self.user.pk,
                    'picture': None,
                    'subscribe': False
                 },
                 {
                    'description': None,
                    'id': course2.pk,
                    'lessons': [],
                    'name': 'test list 2',
                    'num_lessons': 0,
                    'owner': self.user.pk,
                    'picture': None,
                    'subscribe': False
                 }]})
        # Проверка количества записей в БД
        self.assertEqual(Course.objects.filter(owner=self.user).count(), 2)

    def test_retrieve_view_course(self):
        """Тест детального просмотра курса"""
        course = Course.objects.create(name="Test retrieve view course", owner=self.user)
        # Эндпоинт для просмотра курса
        url = reverse('lms:course-detail', args=[course.pk])

        response = self.client.get(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {'description': None,
             'id': course.pk,
             'lessons': [],
             'name': 'Test retrieve view course',
             'num_lessons': 0,
             'owner': self.user.pk,
             'picture': None,
             'subscribe': False})

    def test_update_course(self):
        """Тест изменения курса"""
        course = Course.objects.create(name="Test update course", owner=self.user)
        # Эндпоинт для изменения курса
        url = reverse('lms:course-detail', args=[course.pk])

        response = self.client.patch(path=url, data={"name": "Test update course success"})
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {'description': None,
             'id': course.pk,
             'lessons': [],
             'name': 'Test update course success',
             'num_lessons': 0,
             'owner': self.user.pk,
             'picture': None,
             'subscribe': False})

        response = self.client.put(path=url, data={"name": "Test update course using PUT"})
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка ответа
        self.assertEqual(
            response.json(),
            {'description': None,
             'id': course.pk,
             'lessons': [],
             'name': 'Test update course using PUT',
             'num_lessons': 0,
             'owner': self.user.pk,
             'picture': None,
             'subscribe': False})

    def test_delete_course(self):
        """Тест удаления курса"""
        course = Course.objects.create(name="Test delete course", owner=self.user)
        # Эндпоинт для удаления курса
        url = reverse('lms:course-detail', args=[course.pk])
        # Проверка наличия объекта в БД
        self.assertTrue(Course.objects.all().exists())

        response = self.client.delete(path=url)
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка отсутствия объекта в БД
        self.assertFalse(Course.objects.all().exists())
