from datetime import datetime
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse,
    HttpResponseRedirect
)
from django.shortcuts import (
    render,
    redirect
)

from .forms import UserCreationForm
from .igdb_api import IgdbApi
from .twitter_api import TwitterApi
from .models import (
    Must,
    User
)

igdb = IgdbApi(settings.USER_KEY)


def home(request):
    games = igdb.get_games()
    platforms = igdb.get_platforms()
    genres = igdb.get_genres()
    return render(request, "api/home.html", locals())


def get_particle_games(request, offset):
    games = igdb.get_games(offset=int(offset))
    return JsonResponse({'games': games})


@login_required(login_url='/login')
def must(request):
    user = User.objects.get(username=request.user)
    games_parts = user.get_separated_musts()
    games = []
    for part in games_parts:
        games += igdb.get_games({'id': part})

    return render(request, "api/must.html", {'games': games})


@login_required(login_url='/login')
def create_must(request, game_id):
    user = User.objects.get(username=request.user)
    must_game = list(Must.objects.filter(owner=user, game_id=game_id))
    if must_game:
        return JsonResponse({'Status': 'This must already exist'})

    must_game = Must(owner=user, game_id=game_id)
    must_game.save()
    return JsonResponse({'Status': 'OK'})


@login_required(login_url='/login')
def remove_must(request, game_id):
    user = User.objects.get(username=request.user)
    must_game = Must.objects.filter(owner=user, game_id=game_id)
    must_game.delete()
    return JsonResponse({'Status': 'OK'})


def game_description(request, game_id):
    result = igdb.get_game(game_id)
    if result:
        game = result[0]
        twitter_api = TwitterApi(settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                                 settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

        tweets = twitter_api.search(game['name'])
        tweets = [{'text': tweet['full_text'], 'user': tweet['user']['screen_name'],
                   'date': datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%m.%d.%y %H:%M')}
                  for tweet in tweets] if tweets else None

    return render(request, "api/game.html", {'game': game, 'tweets': tweets})


def search(request, search_string):
    games = igdb.get_games(search_name=search_string)
    return JsonResponse({'games': games})


def filtered_games(request):
    games_filter = {
        'platforms': request.POST.getlist("platforms"),
        'genres': request.POST.getlist("genres"),
        'rating': request.POST.get("rating")
    }
    offset = int(request.POST.get("filter-page"))
    games = igdb.get_games(filter_dict=games_filter, offset=int(offset))
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

        return render(request, "account/login.html", {'Errors': ['Password or login are incorrect']})

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

