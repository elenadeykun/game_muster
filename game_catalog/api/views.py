import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, forms
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

from .forms import UserCreationForm
from .igdb_api import IgdbApi
from .models import Must, User


igdb = IgdbApi(settings.USER_KEY)


def home(request):
    games = igdb.get_games()
    platforms = igdb.get_platforms()
    genres = igdb.get_genres()
    return render(request, "api/home.html", locals())


def get_particle_games(request, offset):
    if int(offset) <= 5:
        games = igdb.get_games(offset=int(offset))
    return JsonResponse({'games': games})


@login_required(login_url='/#login-modal')
def must(request):
    user = User.objects.get(username=request.user)
    must_games = [str(elem.game_id) for elem in Must.objects.filter(owner=user)]

    parts = ((lambda array, n=10: [array[i:i + n] for i in range(0, len(array), n)])(list(must_games)) if must_games
             else [])

    games = []
    for part in parts:
        games += igdb.get_games({'id': part})

    return render(request, "api/must.html", {'games': games})


@login_required(login_url='/#login-modal')
def create_must(request, game_id):
    user = User.objects.get(username=request.user)
    must_game = list(Must.objects.filter(owner=user, game_id=game_id))
    if must_game:
        return JsonResponse({'Status': 'This must already exist'})

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
    return render(request, "api/game.html", {'game': game})


def search(request, search_string):
    games = igdb.get_games(search_name=search_string)
    return JsonResponse({'games': games})


def filtered_games(request):
    games_filter = {
        'platforms': request.POST.getlist("platforms"),
        'genres': request.POST.getlist("genres"),
        'rating': request.POST.get("rating")
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

                return HttpResponseRedirect("/")

        return render(request, "account/login.html", {'Errors': 'Password or login are incorrect'})

    return render(request, "account/login.html")


def logout(request):
    auth.logout(request)
    return JsonResponse({"Status": "OK"})


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

