from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate

from .igdb_api import IgdbApi

# ???????
igdb = IgdbApi("abc48a8eab1764bc6ce6791e6cb1ab9f")


def home(request):
    games = igdb.get_games()
    platforms = igdb.get_platforms()
    genres = igdb.get_genres()
    return render(request, "api/home.html", locals())


def must(request):
    games = igdb.get_games()
    return render(request, "api/must.html", locals())


def game_description(request, game_id):
    result = igdb.get_game(game_id)
    game = result[0] if result else None
    return render(request, "api/game.html", locals())


def filtered_games(request):
    games_filter = {
        'platforms': request.GET.getlist("platforms"),
        'genres': request.GET.getlist("genres"),
        'rating': request.GET.get("rating")
    }
    games = igdb.get_games(games_filter)
    return JsonResponse({"games": games})


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return JsonResponse({'Status': 'OK'})
    else:
        return JsonResponse({'Status': 'Failed'})


def logout(request):
    auth.logout(request)
    return JsonResponse({"Status": "OK"})

