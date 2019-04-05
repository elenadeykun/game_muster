from datetime import datetime

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    JsonResponse,
    HttpResponseRedirect
)
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from api.tasks import save_games
from .forms import UserCreationForm
from .models import (
    Must,
    User,
    Game, Genre, Platform)
from .tokens import account_activation_token
from .utils import send_mail
from .wrappers.igdb_api import IgdbApi
from .wrappers.twitter_api import TwitterApi

igdb = IgdbApi(settings.IGDB_API_KEYS['USER_KEY'])
twitter_api = TwitterApi(settings.TWITTER_API_KEYS['CONSUMER_KEY'],
                         settings.TWITTER_API_KEYS['CONSUMER_SECRET'],
                         settings.TWITTER_API_KEYS['ACCESS_TOKEN'],
                         settings.TWITTER_API_KEYS['ACCESS_TOKEN_SECRET'])


def home(request):
    games = Game.objects.all().values('id', 'name', 'image__url').distinct()[:settings.RECORDS_LIMIT]
    platforms = Platform.objects.all()
    genres = Genre.objects.all()
    return render(request, "api/home.html", locals())


def get_particle_games(request, offset):
    offset *= settings.RECORDS_LIMIT
    games = Game.objects.all().values('id', 'name', 'image__url').distinct()[offset:offset + settings.RECORDS_LIMIT]
    return JsonResponse({'games': [game for game in games]})


@login_required(login_url='/login')
def must(request):
    user = User.objects.get(username=request.user)

    musts = Must.objects.filter(owner=user).values('game', 'game__name', 'game__image__url').distinct('game__name')
    return render(request, "api/must.html", {'musts': musts})


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
    game = Game.objects.get(pk=game_id)

    if game:
        tweets = twitter_api.search(game.name)
        return render(request, "api/game.html", {'game': game, 'tweets': tweets})
    else:
        return render(request, "message_page.html",
                      {'message': 'This game does not exist.'})


def search(request, search_string):
    games = Game.objects.filter(name__icontains=search_string).values('name', 'image__url').distinct('name')
    return JsonResponse({'games': [game for game in games]})


def filtered_games(request):
    search_string = request.POST.get("filter-search-string")
    offset = int(request.POST.get("filter-page"))
    platforms = request.POST.getlist("platforms")
    genres = request.POST.getlist("genres")

    games = Game.objects.filter(users_rating__gte=float(request.POST.get('rating')))

    if platforms:
        games = games.filter(platforms__id__in=[int(platform) for platform in platforms])

    if genres:
        games = games.filter(genres__id__in=[int(genre) for genre in genres])

    if search_string:
        games = games.filter(name__icontains=search_string)

    offset *= settings.RECORDS_LIMIT
    games = games.values('id', 'name', 'image__url').distinct('name')[offset:offset + settings.RECORDS_LIMIT]

    return JsonResponse({"games": [game for game in games]})


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('account/activate_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'

            send_mail(form.cleaned_data.get('email'), mail_subject, message)
            return render(request, "message_page.html",
                          {'message': 'Please confirm your email address to complete the registration'})

    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, "message_page.html", {'message': 'Activation link is invalid!'})
