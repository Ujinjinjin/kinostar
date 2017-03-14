from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^sessions/(?P<filter_by>[a-zA_Z]+)/$', views.sessions, name='sessions'),
    url(r'^create_movie/$', views.create_movie, name='create_movie'),
    url(r'^(?P<album_id>[0-9]+)/create_session/$', views.create_session, name='create_session'),
    url(r'^(?P<album_id>[0-9]+)/delete_session/(?P<song_id>[0-9]+)/$', views.delete_session, name='delete_session'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_movie/$', views.delete_movie, name='delete_movie'),
    url(r'^contacts/$', views.contacts, name='contacts')
]
