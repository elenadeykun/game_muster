from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import (
    JsonResponse,
    HttpResponseRedirect)
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from api.models import Game, Platform, Genre
from .forms import UserCreationForm
from .models import (
    Must,
    User
)
from .tokens import account_activation_token
from api.utils.utils import send_mail
from .wrappers.igdb_api import IgdbApi
from .wrappers.twitter_api import TwitterApi

igdb = IgdbApi(settings.IGDB_API_KEYS['USER_KEY'])
twitter_api = TwitterApi(settings.TWITTER_API_KEYS['CONSUMER_KEY'],
                         settings.TWITTER_API_KEYS['CONSUMER_SECRET'],
                         settings.TWITTER_API_KEYS['ACCESS_TOKEN'],
                         settings.TWITTER_API_KEYS['ACCESS_TOKEN_SECRET'])


def home(request):
    games = (Game.objects.all().values('id', 'name', 'images__url').order_by('name', 'users_rating')
             .distinct('name')[:settings.RECORDS_LIMIT])

    platforms = Platform.objects.all()
    genres = Genre.objects.all()
    if request.user.is_authenticated:
        musts = [must['game__id'] for must in Must.objects.filter(owner=request.user).values('game__id')]

    return render(request, "api/home.html", locals())


def get_particle_games(request, offset):
    offset *= settings.RECORDS_LIMIT
    games = (Game.objects.all().values('id', 'name', 'images__url').order_by('name', 'users_rating')
                 .distinct('name')[offset:offset + settings.RECORDS_LIMIT])
    return JsonResponse({'games': [game for game in games]})


@login_required(login_url='/login')
def must(request):
    user = User.objects.get(username=request.user)
    musts = []
    for must in Must.objects.filter(owner=user).order_by('game__name', 'game__user_rating').distinct('game__name'):
        musts.append({'id': must.game.id,
                      'name': must.game.name,
                      'image': must.game.images.all()[0].url if must.game.images.all() else None,
                      'count': must.count})

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
    images = [image.url for image in game.images.all()]
    platforms = [platform.name for platform in game.platforms.all()]
    genres = [genre.name for genre in game.genres.all()]

    if request.user.is_authenticated and Must.objects.filter(owner=request.user, game=game).count() > 0:
        in_must = True

    if game:
        tweets = twitter_api.search(game.name)
        return render(request, "api/game.html", locals())
    else:
        return render(request, "message_page.html",
                      {'message': 'This game does not exist.'})


def search(request, search_string):
    games = (Game.objects.filter(name__icontains=search_string).values('id', 'name', 'images__url')
             .order_by('name', 'users_rating').distinct('name'))
    return JsonResponse({'games': [game for game in games]})


def filtered_games(request):
    search_string = request.POST.get("filter-search-string")
    offset = int(request.POST.get("filter-page"))
    platforms = request.POST.getlist("platforms")
    genres = request.POST.getlist("genres")

    filters = Q(users_rating__gte=float(request.POST.get('rating')))

    if search_string:
        filters.add(Q(name__icontains=search_string), Q.AND)

    if platforms:
        filters.add(Q(platforms__id__in=[int(platform) for platform in platforms]), Q.AND)

    if genres:
        filters.add(Q(genres__id__in=[int(genre) for genre in genres]), Q.AND)

    games = Game.objects.filter(filters)
    offset *= settings.RECORDS_LIMIT
    games = (games.values('id', 'name', 'images__url').order_by('name', 'users_rating')
             .distinct('name')[offset:offset + settings.RECORDS_LIMIT])

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

        return render(request, "api/account/login.html", {'Errors': ['Password or login are incorrect']})

    return render(request, "api/account/login.html")


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
            message = render_to_string('api/account/activate_mail.html', {
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
    return render(request, 'api/account/register.html', {'form': form})


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
