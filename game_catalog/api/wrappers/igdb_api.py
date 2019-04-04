import json
import requests
from django.conf import settings


class IgdbApi:
    FIELDS = ['name', 'screenshots.url', 'summary', 'release_dates.date', 'rating', 'aggregated_rating',
              'genres.name', 'platforms.abbreviation', 'rating_count', 'tags', 'updated_at',
              'aggregated_rating_count']

    def __init__(self, user_key):
        self.__api_url = "https://api-v3.igdb.com/"
        self.__query_header = {'user-key': user_key}

    @staticmethod
    def __get_parameter(parameter, value, option="="):
        data = ("where {parameter} {option} {value}; ".format(parameter=parameter, option=option, value=value)
                if value else '')
        return data

    def get_game(self, game_id):
        url = self.__api_url + "games/"

        data = "fields " + ",".join(self.FIELDS) + "; "
        data += IgdbApi.__get_parameter('id', game_id)

        response = requests.post(url, headers=self.__query_header, data=data)

        return json.loads(response.text) if response.status_code is settings.SUCCESS_STATUS else None

    def get_games(self, filter_dict={}, offset=0, limit=settings.RECORDS_LIMIT,  search_name=''):
        url = self.__api_url + "games/"
        data = "fields " + ",".join(self.FIELDS) + "; "

        if search_name:
            data += 'search "{name}"; '.format(name=search_name)

        for key in filter_dict:
            value = ",".join(filter_dict[key]) if filter_dict[key] else None
            value = '(' + value + ')' if filter_dict[key] and len(filter_dict[key]) > 1 else value

            data += (IgdbApi.__get_parameter(key, value, '>') if key is "rating"
                     else IgdbApi.__get_parameter(key, value))

        if not search_name:
            data += " sort popularity desc; limit {limit}; offset {offset};".format(limit=limit, offset=offset*limit)

        response = requests.post(url, headers=self.__query_header, data=data)

        return json.loads(response.text) if response.status_code is settings.SUCCESS_STATUS else None

    def get_platforms(self):
        url = self.__api_url + "platforms/"
        data = "fields abbreviation;"
        response = requests.post(url, headers=self.__query_header, data=data)

        return json.loads(response.text) if response.status_code is settings.SUCCESS_STATUS else None

    def get_genres(self):
        url = self.__api_url + "genres/"
        data = "fields name;"
        response = requests.post(url, headers=self.__query_header, data=data)

        return json.loads(response.text) if response.status_code is settings.SUCCESS_STATUS else None
