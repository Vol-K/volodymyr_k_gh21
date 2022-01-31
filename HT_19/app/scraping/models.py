from django.db import models


# Create your models here.
class Askstories(models.Model):
    by = models.CharField(max_length=100, default="")
    descendants = models.IntegerField(default="")
    id_item = models.PositiveIntegerField(default=0)
    kids = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    score = models.IntegerField(default="")
    time = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.title


class Showstories(models.Model):
    by = models.CharField(max_length=100, default="")
    descendants = models.IntegerField(default="")
    id_item = models.PositiveIntegerField(default=0)
    kids = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    score = models.IntegerField(default="")
    time = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=60, default="")
    url = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title


class Newstories(models.Model):
    by = models.CharField(max_length=100, default="")
    descendants = models.IntegerField(default="")
    id_item = models.PositiveIntegerField(default=0)
    kids = models.TextField(default="", blank=True)
    text = models.TextField(default="", blank=True)
    score = models.IntegerField(default="")
    time = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=60, default="")
    url = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title


class Jobstories(models.Model):
    by = models.CharField(max_length=100, default="")
    id_item = models.PositiveIntegerField(default=0)
    text = models.TextField(default="", blank=True)
    score = models.IntegerField(default="")
    time = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=60, default="")
    url = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title
