from django.test import TestCase
from rest_framework.test import APIClient
from education.models import Lesson, LessonView
from django.contrib.auth.models import User
from education.serializers import LessonWithStatusSerializer, LessonSerializer
from product.models import Product, Access

""" In this cases creating objects in models
 and serialize it with serializators 
 and check that is correctly was created """


class LessonSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', url='https://example.com', duration=600)
        self.access = Access.objects.create(user=self.user, product=self.product)
        self.lesson_view = LessonView.objects.create(user=self.user, lesson=self.lesson, viewed=True,
                                                     view_time_seconds=600)

    def test_lesson_serializer(self):
        self.client.force_authenticate(user=self.user)
        request = self.client.get('/api/lesson/').wsgi_request
        serializer = LessonSerializer(self.lesson, context={'request': request, 'user': self.user})
        data = serializer.data

        self.assertEqual(data['id'], self.lesson.id)
        self.assertEqual(data['title'], self.lesson.title)
        self.assertEqual(data['url'], self.lesson.url)
        self.assertEqual(data['duration'], self.lesson.duration)
        self.assertEqual(data['viewed'], True)
        self.assertEqual(data['view_time_seconds'], 600)


class LessonWithStatusSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', url='https://example.com', duration=600)
        self.access = Access.objects.create(user=self.user, product=self.product)
        self.lesson_view = LessonView.objects.create(user=self.user, lesson=self.lesson, viewed=True,
                                                     view_time_seconds=600)

    def test_lesson_serializer(self):
        self.client.force_authenticate(user=self.user)
        request = self.client.get(f'/api/lessonviewed/{self.product.id}/').wsgi_request
        serializer = LessonWithStatusSerializer(self.lesson, context={'request': request, 'user': self.user})
        data = serializer.data

        self.assertEqual(data['id'], self.lesson.id)
        self.assertEqual(data['title'], self.lesson.title)
        self.assertEqual(data['url'], self.lesson.url)
        self.assertEqual(data['duration'], self.lesson.duration)
        self.assertEqual(data['viewed'], True)
        self.assertEqual(data['view_time_seconds'], 600)
        self.assertIsNotNone(data['last_view_date'])
