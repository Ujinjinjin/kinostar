from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):

    movie_title = models.CharField(max_length=250)
    movie_logo = models.FileField(default=None)
    trailer = models.CharField(max_length=500, default='')
    about = models.CharField(max_length=2000, default='')
    genre = models.CharField(max_length=100, default=None)
    duration = models.IntegerField(default=0)
    age_limit = models.IntegerField(default=0)
    production = models.CharField(max_length=100, default=None)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.movie_title


class Song(models.Model):
    movie = models.ForeignKey(Album, on_delete=models.CASCADE)
    session_time = models.CharField(max_length=250, default=None)
    price = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.session_time
