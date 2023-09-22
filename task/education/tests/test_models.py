from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from education.models import Lesson, LessonView
from product.models import Product, Access

""" Creating objects in models and
 making sure that's was created correctly """


class ProductModelTestCase(TestCase):
    """ Test for Product model """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_product_creation(self):
        product = Product.objects.create(product_name='Test Product', owner=self.user)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.owner, self.user)


class AccessModelTestCase(TestCase):
    """ Test for Access model """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)

    def test_access_creation(self):
        access = Access.objects.create(user=self.user, product=self.product)
        self.assertEqual(access.user, self.user)
        self.assertEqual(access.product, self.product)


class LessonModelTestCase(TestCase):
    """ Test for Lesson model """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(product_name='Test Product', owner=self.user)

    def test_lesson_creation(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            url='https://example.com',
            duration=600
        )
        lesson.products.add(self.product)

        self.assertEqual(lesson.title, 'Test Lesson')
        self.assertEqual(lesson.url, 'https://example.com')
        self.assertEqual(lesson.duration, 600)
        self.assertIn(self.product, lesson.products.all())


class LessonViewModelTestCase(TestCase):
    """ Test for LessonView model """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            url='https://example.com',
            duration=600
        )

    def test_lesson_view_creation(self):
        lesson_view = LessonView.objects.create(
            user=self.user,
            lesson=self.lesson,
            viewed=True,
            view_time_seconds=600,
            view_date=timezone.now()
        )

        self.assertEqual(lesson_view.user, self.user)
        self.assertEqual(lesson_view.lesson, self.lesson)
        self.assertTrue(lesson_view.viewed)
        self.assertEqual(lesson_view.view_time_seconds, 600)
        self.assertIsNotNone(lesson_view.view_date)
