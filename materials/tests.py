from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@test.com')
        self.course = Course.objects.create(name='CourseTest',
                                            description='CourseTest description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name='LessonTest',
                                            description='LessonTest description',
                                            course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('materials:lessons_create')
        data = {
            'name': 'New Lesson',
            'description': 'New Lesson description',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'name': self.lesson.name, 'image': None, 'description': self.lesson.description,
             'url': None, 'course': self.course.pk, 'owner': self.user.pk}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], self.lesson.name)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            'name': 'New Test Lesson'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'New Test Lesson')

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@test.com')
        self.course = Course.objects.create(name='CourseTest',
                                            description='CourseTest description',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse('materials:subscription_create')
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data,  {'message': 'Подписка добавлена'})

    def test_unsubscribe(self):
        url = reverse('materials:subscription_create')
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data,  {'message': 'Подписка удалена'})