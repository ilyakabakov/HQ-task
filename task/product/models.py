from django.contrib.auth.models import User
from django.db import models

""" First part of Tasks """


class Product(models.Model):
    """ Создать сущность продукта.
     У продукта должен быть владелец. """

    product_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Access(models.Model):
    """ Необходимо добавить сущность
     для сохранения доступов к продукту для пользователя. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.username} - {self.product.product_name}"
