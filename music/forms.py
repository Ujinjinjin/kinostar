from django import forms
from django.contrib.auth.models import User

from .models import Album, Song


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['movie_title', 'movie_logo', 'trailer', 'about', 'genre',
                  'duration', 'age_limit', 'production', 'is_favorite']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['movie', 'session_time', 'price', 'is_favorite']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
