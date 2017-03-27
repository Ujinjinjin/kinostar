from django.contrib.auth.models import Permission, User
from django.db import models


class Movie(models.Model):

    movie_title = models.CharField(max_length=250)
    movie_logo = models.FileField(default=None)
    trailer = models.CharField(max_length=500, default='')
    about = models.CharField(max_length=2000, default='')
    genre = models.CharField(max_length=100, default=None)
    duration = models.IntegerField(default=0)
    age_limit = models.IntegerField(default=0)
    production = models.CharField(max_length=100, default=None)
    premier_date = models.DateField(default=None)
    is_announcement = models.BooleanField(default=False)

    def __str__(self):
        return self.movie_title


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    session_time = models.CharField(max_length=250, default=None)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.session_time


class EmbedText(models.Model):
    text = models.CharField(max_length=100)
    page_name = models.CharField(max_length=25)

    def __str__(self):
        return '{}: {}'.format(self.page_name, self.text)
