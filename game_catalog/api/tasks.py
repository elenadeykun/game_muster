from datetime import datetime

from django.conf import settings

from .models import Must, Game, Genre, Platform, Image, Rating
from .utils import split
from .wrappers.igdb_api import IgdbApi

igdb = IgdbApi(settings.IGDB_API_KEYS['USER_KEY'])


def save_users_musts():
    PART_LENGTH = 10

    musts = Must.objects.values("game_id")
    musts_parts = split([str(elem['game_id']) for elem in musts], PART_LENGTH)
    games = []

    for part in musts_parts:
        games += igdb.get_games({'id': part})


def save_parameter(game, model, parameter, value):
    elements = []

    if game.get(parameter):
        for elem in game.get(parameter):
            elem_db, created = model.objects.get_or_create(name=elem[value])
            elements.append(elem_db)

    return elements


def save_games(games):
    for game in games:
        release_date = (datetime.fromtimestamp(game['release_dates'][-1]['date'])
                        if 'release_dates' in game else None)

        game_db, created = Game.objects.get_or_create(name=game['name'], description=game.get('description'),
                                                      release_date=release_date)

        if created:
            genres = save_parameter(game, Genre, 'genres', 'name')
            platforms = save_parameter(game, Platform, 'platforms', 'abbreviation')

            game_db.genres.set(genres)
            game_db.platforms.set(platforms)
            game_db.save()

            rating = Rating(users_rating=float(game.get('rating', 0)),
                            critics_rating=float(game.get('aggregated_rating', 0)),
                            users_views=int(game.get('rating_count', 0)),
                            critics_views=int(game.get('aggregated_rating_count', 0)),
                            game=game_db)
            rating.save()

            screenshots = []

            if game.get('screenshots'):
                for screen in game.get('screenshots'):
                    screen_db, created = Image.objects.get_or_create(url=screen['url'], game=game_db)
                    screenshots.append(screen_db)
