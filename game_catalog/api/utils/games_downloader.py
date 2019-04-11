import logging
from datetime import datetime

from django.conf import settings

from api.models import Game, Genre, Platform, Image
from api.wrappers.igdb_api import IgdbApi


class GamesDownloader:

    def __init__(self):
        self.igdb = IgdbApi(settings.IGDB_API_KEYS['USER_KEY'])

    def __save_instance(self, game, model, parameter, value):
        elements = []

        if game.get(parameter):
            for elem in game.get(parameter):
                if elem.get(value):
                    elem_db, created = model.objects.get_or_create(name=elem[value])
                    elements.append(elem_db)

        return elements

    def __save_genres(self, game):
        return self.__save_instance(game, Genre, 'genres', 'name')

    def __save_platforms(self, game):
        return self.__save_instance(game, Platform, 'platforms', 'abbreviation')

    def __save_game(self, game):
        logging.debug(game.get('release_dates'))
        release_date = (datetime.fromtimestamp(game['release_dates'][-1]['date'])
                        if 'release_dates' in game and game['release_dates'][-1].get('date') else None)

        is_game_exist = Game.objects.filter(name=game['name']).first()

        if not is_game_exist:
            game_db, created = Game.objects.get_or_create(name=game['name'], description=game.get('summary'),
                                                          release_date=release_date,
                                                          users_rating=float(game.get('rating', 0)),
                                                          critics_rating=float(game.get('aggregated_rating', 0)),
                                                          users_views=int(game.get('rating_count', 0)),
                                                          critics_views=int(game.get('aggregated_rating_count', 0)))

            genres = self.__save_genres(game)
            platforms = self.__save_platforms(game)
            if genres:
                game_db.genres.set(genres)
            if platforms:
                game_db.platforms.set(platforms)
            game_db.save()

            screenshots = []

            if game.get('screenshots'):
                for screen in game.get('screenshots'):
                    screen_db, created = Image.objects.get_or_create(url=screen['url'], game=game_db)
                    screenshots.append(screen_db)

    def download(self):
        offset = Game.objects.all().count() // settings.GAMES_DOWNLOAD_LIMIT

        games = self.igdb.get_games(offset=offset, limit=settings.GAMES_DOWNLOAD_LIMIT)
        if games:
            for game in games:
                self.__save_game(game)
