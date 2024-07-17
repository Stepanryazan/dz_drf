from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)  # Аутентифицируем клиента с созданным пользователем

        self.lesson = Lesson.objects.create(
            title='Lesson_test_1',
            description='Test_1',
            link_to_video="https://youtube.com/lesson_test_1/",
            owner=self.user
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""
        lesson = {
            "title": "Lesson_test_2",
            "description": "Test_2",
            "link_to_video": "https://youtube.com/lesson_test_2/"
        }
        response = self.client.post(
            '/lesson/create/',
            data=lesson
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'id': 2,
                'title': 'Lesson_test_2',
                'preview_image': None,
                'description': 'Test_2',
                'link_to_video': 'https://youtube.com/lesson_test_2/',
                'course': None,
                'owner': 1
            }
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_create_lesson_validation_error(self):
        """Тестирование валидации при создании урока"""
        lesson = {
            "title": "Lesson_test_2",
            "description": "Test_2",
            "link_to_video": "https://you.com/lesson_test_2/"
        }
        response = self.client.post(
            '/lesson/create/',
            data=lesson
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "You can only add links to videos on youtube.com"
                ]
            }
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.id,
                        'title': 'Lesson_test_1',
                        'preview_image': None,
                        'description': 'Test_1',
                        'link_to_video': 'https://youtube.com/lesson_test_1/',
                        'course': None,
                        'owner': self.lesson.owner.id
                    }
                ]
            }
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""

        data = {
            "title": "Lesson_test_1_update",
            "description": "Test_1",
            "link_to_video": "https://youtube.com/lesson_test_1/",
            "owner": self.lesson.owner.id
        }

        response = self.client.patch(
            f'/lesson/update/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'Lesson_test_1_update',
                'preview_image': None,
                'description': 'Test_1',
                'link_to_video': 'https://youtube.com/lesson_test_1/',
                'course': None,
                'owner': self.lesson.owner.id
            }
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response = self.client.delete(
            f'/lesson/delete/{self.lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Course_test_1',
            description='Test_1',
            owner=self.user
        )

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        subscription = {
            "user": self.user.id,
            "course": self.course.id,
            "is_activ": True
        }
        response = self.client.post(
            f'/course/{self.course.id}/subscription/create/',
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'is_activ': True, 'user': self.user.id, 'course': 1}
        )

        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_delete_subscription(self):
        """Тестирование удаления подписки"""

        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_activ=True
        )

        response = self.client.delete(
            f'/course/subscription/{subscription.id}/delete/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )