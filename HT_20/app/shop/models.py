from django.db import models


# Models for the three types of products on the website.
class TeleVision(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")


class Phones(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")


class PersonalComputers(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")


class ProduntsInCart(models.Model):
    user_id = models.PositiveIntegerField(default=0)
    prod_id = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20)
    amount = models.PositiveIntegerField(default=0)
    price_one_product = models.PositiveIntegerField(default=0)