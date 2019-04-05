import logging
from datetime import datetime

from django.conf import settings

from game_catalog.celery import app
from .models import Game, Genre, Platform, Image
from .wrappers.igdb_api import IgdbApi

igdb = IgdbApi(settings.IGDB_API_KEYS['USER_KEY'])


@app.task
def save_games():
    LIMIT = 20

    offset = Game.objects.all().count() // LIMIT

    games = igdb.get_games(offset=offset, limit=LIMIT)
    if games:
        for game in games:
            save_game(game)


def save_parameter(game, model, parameter, value):
    elements = []

    if game.get(parameter):
        for elem in game.get(parameter):
            if elem.get(value):
                elem_db, created = model.objects.get_or_create(name=elem[value])
                elements.append(elem_db)

    return elements


def save_game(game):
    logging.debug(game.get('release_dates'))
    release_date = (datetime.fromtimestamp(game['release_dates'][-1]['date'])
                    if 'release_dates' in game and game['release_dates'][-1].get('date') else None)

    game_db, created = Game.objects.get_or_create(name=game['name'], description=game.get('summary'),
                                                  release_date=release_date,
                                                  users_rating=float(game.get('rating', 0)),
                                                  critics_rating=float(game.get('aggregated_rating', 0)),
                                                  users_views=int(game.get('rating_count', 0)),
                                                  critics_views=int(game.get('aggregated_rating_count', 0)))

    if created:
        genres = save_parameter(game, Genre, 'genres', 'name')
        platforms = save_parameter(game, Platform, 'platforms', 'abbreviation')
        game_db.genres.set(genres)
        game_db.platforms.set(platforms)
        game_db.save()

        screenshots = []

        if game.get('screenshots'):
            for screen in game.get('screenshots'):
                screen_db, created = Image.objects.get_or_create(url=screen['url'], game=game_db)
                screenshots.append(screen_db)

