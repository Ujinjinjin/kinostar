from django.contrib import admin
from .models import Movie, Session, EmbedText

admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(EmbedText)
