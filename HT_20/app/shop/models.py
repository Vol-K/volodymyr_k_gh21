from django.db import models

# Create your models here.


class TeleVisio(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")

    def __str__(self):
        return (" ").join((self.brand, self.model))


class Phones(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")

    def __str__(self):
        return (" ").join((self.brand, self.model))


class PersonalComputers(models.Model):
    brand = models.CharField(max_length=20, default="")
    model = models.CharField(max_length=100, default="")
    description = models.TextField(default="", blank=True)
    price = models.PositiveIntegerField(default=0)
    available = models.CharField(max_length=3, default="No")

    def __str__(self):
        return (" ").join((self.brand, self.model))
