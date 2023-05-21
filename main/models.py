from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    fio = models.CharField(max_length=120)
    username = models.CharField(max_length=120)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    price = models.PositiveIntegerField()


class Cart(models.Model):
    products = models.ManyToManyField(Product, related_name='cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_price = models.PositiveIntegerField()
