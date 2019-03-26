import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .forms import UserCreationForm
from .igdb_api import IgdbApi
from .models import Must, User


igdb = IgdbApi(settings.USER_KEY)


def home(request):
    games = igdb.get_games()
    platforms = igdb.get_platforms()
    genres = igdb.get_genres()
    register_form = UserCreationForm()
    return render(request, "api/home.html", locals())


def get_particle_games(request, offset):
    games = igdb.get_games(offset=offset)
    return JsonResponse({'games': games})


@login_required(login_url='/#login-modal')
def must(request):
    user = User.objects.get(username=request.user)
    must_games = [str(elem.game_id) for elem in Must.objects.filter(owner=user)]
    games = igdb.get_games({'id': must_games}) if must_games else None
    return render(request, "api/must.html", locals())


@login_required(login_url='/#login-modal')
def create_must(request, game_id):
    user = User.objects.get(username=request.user)
    must_game = Must(owner=user, game_id=game_id)
    must_game.save()
    return JsonResponse({'Status': 'OK'})


@login_required(login_url='/#login-modal')
def remove_must(request, game_id):
    user = User.objects.get(username=request.user)
    must_game = Must.objects.filter(owner=user, game_id=game_id)
    must_game.delete()
    return JsonResponse({'Status': 'OK'})


def game_description(request, game_id):
    result = igdb.get_game(game_id)
    game = result[0] if result else None
    return render(request, "api/game.html", locals())


def search(request):
    games = igdb.get_games(search_name=request.GET.get('search_string'))
    return JsonResponse({'games': games})


def filtered_games(request):
    games_filter = {
        'platforms': request.GET.getlist("platforms"),
        'genres': request.GET.getlist("genres"),
        'rating': request.GET.get("rating")
    }
    games = igdb.get_games(games_filter)
    return JsonResponse({"games": games})


def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return JsonResponse({'Status': 'OK',
                                     'user': {'username': user.username,
                                              'email': user.email,
                                              'last_name': user.last_name,
                                              'first_name': user.first_name}
                                     })

        return JsonResponse({'Errors': 'Password or login are incorrect'})

    return JsonResponse({'Status': 'Failed'})


def logout(request):
    auth.logout(request)
    return JsonResponse({"Status": "OK"})


def registration(request):
    form = UserCreationForm(request.POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return JsonResponse({'Status': 'OK',
                                     'user': {'username': user.username,
                                              'email': user.email,
                                              'last_name': user.last_name,
                                              'first_name': user.first_name}
                                     })

    return JsonResponse({'Errors': list(form.error_messages.values())})


