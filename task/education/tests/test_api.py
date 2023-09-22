from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from education.models import Lesson, LessonView
from product.models import Product, Access

""" In this cases checking what is
 correctly create lists 
 and HTTP response is 200(OK) """


class LessonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', url='https://example.com', duration=600)
        self.access = Access.objects.create(user=self.user, product=self.product)
        self.client.force_authenticate(user=self.user)

    def test_get_lessons_with_status(self):
        response = self.client.get('/api/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lessons_with_status_for_product(self):
        response = self.client.get(f'/api/lessonviewed/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_statistics(self):
        response = self.client.get('/api/statistic/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonWithStatusAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', url='https://example.com', duration=600)
        self.access = Access.objects.create(user=self.user, product=self.product)
        self.lesson_view = LessonView.objects.create(user=self.user, lesson=self.lesson, viewed=True,
                                                     view_time_seconds=600)

    def test_get_lessons_with_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lessons_with_status_for_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/lessonviewed/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductStatisticsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.access = Access.objects.create(user=self.user, product=self.product)
        self.lesson = Lesson.objects.create(title='Test Lesson', url='https://example.com', duration=600)
        self.lesson_view = LessonView.objects.create(user=self.user, lesson=self.lesson, viewed=True,
                                                     view_time_seconds=600)

    def test_get_product_statistics(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/statistic/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
