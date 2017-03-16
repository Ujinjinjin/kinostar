from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song

VIDEO_FILE_TYPES = ['mp4', 'avi']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_movie(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.movie_logo = request.FILES['movie_logo']
            file_type = album.movie_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'movie': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_movie.html', context)
            album.save()
            return render(request, 'music/detail.html', {'movie': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_movie.html', context)


def create_session(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.session_time == form.cleaned_data.get("session_time"):
                context = {
                    'movie': album,
                    'form': form,
                    'error_message': 'Сеанс на {} для этого фильма уже создан'.format(s.session_time),
                }
                return render(request, 'music/create_session.html', context)
        song = form.save(commit=False)
        song.album = album

        song.save()
        return render(request, 'music/detail.html', {'movie': album})
    context = {
        'movie': album,
        'form': form,
    }
    return render(request, 'music/create_session.html', context)


def delete_movie(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.all()
    return render(request, 'music/index.html', {'movies': albums})


def delete_session(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'movie': album})


def detail(request, album_id):
    user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'movie': album, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):

    albums = Album.objects.all()
    song_results = Song.objects.all()
    query = request.GET.get("q")
    if query:
        albums = albums.filter(
            Q(album_title__imcontains=query) |
            Q(artist__icontains=query)
        ).distinct()
        song_results = song_results.filter(
            Q(song_title__icontains=query)
        ).distinct()
        return render(request, 'music/index.html', {
            'movies': albums,
            'songs': song_results,
        })
    else:
        return render(request, 'music/index.html', {'movies': albums})


def contacts(request):
    return render(request, 'music/contacts.html')


def logout_user(request):
    logout(request)
    # albums = Album.objects.all()
    return redirect('music:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.all()
                return render(request, 'music/index.html', {'movies': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'movies': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def sessions(request, filter_by):

    try:
        song_ids = []
        for album in Album.objects.all():
            for song in album.song_set.all():
                song_ids.append(song.pk)
        users_songs = Song.objects.filter(pk__in=song_ids)
        if filter_by == 'favorites':
            users_songs = users_songs.filter(is_favorite=True)
    except Album.DoesNotExist:
        users_songs = []
    users_songs = users_songs.order_by('session_time')
    return render(request, 'music/sessions.html', {
        'session_list': users_songs,
        'filter_by': filter_by,
    })
