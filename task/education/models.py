from django.contrib.auth.models import User
from django.db import models

from product.models import Product

""" First part of Tasks """


class Lesson(models.Model):
    """ Создать сущность урока.
    Урок может находиться в нескольких продуктах одновременно.
    В уроке должна быть базовая информация:
    название,
    ссылка на видео,
    длительность просмотра. """

    title = models.CharField(max_length=256)
    url = models.URLField()
    duration = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, related_name='lessons')

    def __str__(self):
        return f'Title: {self.title}'


class LessonView(models.Model):
    """ Урок могут просматривать множество пользователей.
    Необходимо для каждого фиксировать время просмотра
    и фиксировать статус “Просмотрено”/”Не просмотрено”.
    Статус “Просмотрено” проставляется,
    если пользователь просмотрел 80% ролика. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    viewed = models.BooleanField(default=False)
    view_time_seconds = models.PositiveIntegerField(default=0)
    view_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username} Title: {self.lesson.title}"
