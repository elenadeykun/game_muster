from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    JsonResponse,
    HttpResponseRedirect
)
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import permissions, generics, status
from rest_framework.decorators import permission_classes

from api.models import Game, Platform, Genre
from api.serializers import GameSerializer, MustSerializer, PlatformSerializer, \
    GenreSerializer, GameDetailSerializer
from .forms import UserCreationForm
from .models import (
    Must,
    User
)
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
    games = igdb.get_games()
    platforms = igdb.get_platforms()
    genres = igdb.get_genres()

    return render(request, "api/home.html", locals())


@permission_classes((permissions.AllowAny,))
class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


@permission_classes((permissions.AllowAny,))
class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer


@permission_classes((permissions.AllowAny,))
class PlatformList(generics.ListAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


@permission_classes((permissions.AllowAny,))
class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MustList(generics.ListCreateAPIView):
    queryset = Must.objects.all()
    serializer_class = MustSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Must.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        must = Must.objects.filter(owner=self.request.user, game=serializer.validated_data['game']).first()
        if must:
            return status.HTTP_409_CONFLICT
        else:
            serializer.save(owner=self.request.user)


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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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

