from django import forms
from django.contrib.auth.models import User

from .models import Movie, Session


class MovieForm(forms.ModelForm):
    premier_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Movie
        fields = ['movie_title', 'movie_logo', 'trailer', 'about', 'genre',
                  'duration', 'age_limit', 'production', 'premier_date', 'is_announcement']


class SessionForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ['movie', 'session_time', 'price']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
