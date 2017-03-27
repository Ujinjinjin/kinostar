from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import MovieForm, SessionForm, UserForm
from .models import Movie, Session, EmbedText

VIDEO_FILE_TYPES = ['mp4', 'avi']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def announcements(request):
    albums = Movie.objects.filter(is_announcement=True).order_by('premier_date')  # Фильмы сортируются по дате. Я че зря добавил эту фичу?
    embed_text = EmbedText.objects.get(page_name='announcements')
    return render(request, 'music/index.html', {'movies': albums, 'embed_text': embed_text})


def announcement_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    try:
        if movie.is_announcement:
            movie.is_announcement = False
        else:
            movie.is_announcement = True
        movie.save()
    except (KeyError, Movie.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def contacts(request):
    return render(request, 'music/contacts.html')


def create_movie(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = MovieForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)

            trailer = str(album.trailer).replace('watch?v=', 'embed/') + '&'
            trailer = trailer[:trailer.index('&')]
            album.trailer = trailer

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


def create_session(request, movie_id):
    form = SessionForm(request.POST or None, request.FILES or None)
    movie = get_object_or_404(Movie, pk=movie_id)
    if form.is_valid():
        movies_sessions = movie.session_set.all()
        for s in movies_sessions:
            if s.session_time == form.cleaned_data.get("session_time"):
                context = {
                    'movie': movie,
                    'form': form,
                    'error_message': 'Сеанс на {} для этого фильма уже создан'.format(s.session_time),
                }
                return render(request, 'music/create_session.html', context)
        session = form.save(commit=False)
        session.movie = movie

        session.save()
        return render(request, 'music/detail.html', {'movie': movie})
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'music/create_session.html', context)


def delete_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie.delete()
    # albums = Movie.objects.all()
    return redirect('music:index')


def delete_session(request, movie_id, session_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    session = Session.objects.get(pk=session_id)
    session.delete()
    return render(request, 'music/detail.html', {'movie': movie})


def detail(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'music/detail.html', {'movie': movie, 'user': user})


def edit_embed(request, page_name):
    embed = EmbedText.objects.get(page_name=page_name)
    if request.method == "POST":
        new_embed = request.POST['new_embed']
    else:
        new_embed = embed.text
    embed.text = new_embed
    embed.save()
    return redirect('music:{}'.format(page_name))


"""def favorite(request, song_id):
    song = get_object_or_404(Session, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Session.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})"""


def index(request):
    movies = Movie.objects.filter(is_announcement=False).order_by('premier_date')
    embed_text = EmbedText.objects.get(page_name='index')
    return render(request, 'music/index.html', {'movies': movies, 'embed_text': embed_text})


def logout_user(request):
    logout(request)
    # albums = Movie.objects.all()
    return redirect('music:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Movie.objects.all()
                return redirect('music:index')
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
                movies = Movie.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'movies': movies})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def sessions(request):
    try:
        session_ids = []
        for movie in Movie.objects.all():
            for session in movie.session_set.all():
                session_ids.append(session.pk)
        all_sessions = Session.objects.filter(pk__in=session_ids)
        # if filter_by == 'favorites':
        #     all_sessions = all_sessions.filter(is_favorite=True)
    except Movie.DoesNotExist:
        all_sessions = []
    all_sessions = list(all_sessions.order_by('session_time'))

    embed_text = EmbedText.objects.get(page_name='sessions')

    if len(all_sessions) > 0:
        while True:  # Корректировка по времени
            if int(str(all_sessions[0]).split(':')[0]) < 4:  # Все что до 4 утра - ночь
                c = all_sessions[0]  # Запоминаем первый сеанс
                del(all_sessions[0])  # Удаляем его
                all_sessions.append(c)  # Добавляем в конец P.s. Думаю, что так быстрей
            else:
                break

    return render(request, 'music/sessions.html', {
        'session_list': all_sessions,
        # 'filter_by': filter_by,
        'embed_text': embed_text,
    })
