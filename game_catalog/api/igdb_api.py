import requests
import json


class IgdbApi:
    def __init__(self, user_key):
        self.__api_url = "https://api-v3.igdb.com/"
        self.__query_header = {'user-key': user_key}
        self.__data = ''

    def __set_parameter(self, parameter, value, option="="):
        self.__data += ("where {parameter} {option} {value}; ".format(parameter=parameter, option=option, value=value)
                        if value else '')

    def get_game(self, game_id):
        url = self.__api_url + "games/"
        fields = ['name', 'screenshots.url', 'summary', 'release_dates', 'rating', 'aggregated_rating',
                  'genres.name', 'platforms.abbreviation', 'rating_count', 'tags', 'updated_at']
        self.__data = "fields " + ",".join(fields) + "; where id={id};".format(id=game_id)

        return json.loads(requests.post(url, headers=self.__query_header, data=self.__data).text)

    def get_games(self, filter_dict={}):
        url = self.__api_url + "games/"
        fields = ['name', 'screenshots.url']
        self.__data = "fields " + ",".join(fields) + "; "

        for key in filter_dict:
            value = ",".join(filter_dict[key]) if filter_dict[key] else None
            value = '(' + value + ')' if filter_dict[key] and len(filter_dict[key]) > 1 else value

            if key is "rating":
                self.__set_parameter(key, value, '>')
            else:
                self.__set_parameter(key, value)

        return json.loads(requests.post(url, headers=self.__query_header, data=self.__data).text)

    def get_platforms(self):
        url = self.__api_url + "platforms/"
        self.__data = "fields abbreviation;"
        return json.loads(requests.post(url, headers=self.__query_header, data=self.__data).text)

    def get_genres(self):
        url = self.__api_url + "genres/"
        self.__data = "fields name;"
        return json.loads(requests.post(url, headers=self.__query_header, data=self.__data).text)

