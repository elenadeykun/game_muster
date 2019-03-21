import requests
import json

SHORT_DESCRIPTION_FIELDS = 'fields name, screenshots.url; '
LONG_DESCRIPTION_FIELDS = ('fields name, screenshots.url, summary, release_dates, rating, aggregated_rating,' 
                            ' genres.name, platforms.abbreviation, rating_count, tags; ')


class IgdbApi:
    def __init__(self, user_key):
        self.__api_url = "https://api-v3.igdb.com/games/"
        self.__query_header = {'user-key': user_key}
        self.__data = ''

    def set_parameter(self, parameter, value, option="="):
        if option is "=":
            self.__data += ("where {parameter} = {value}; ".format(parameter=parameter, value=value)
                            if value else '')
        elif option is ">":
            self.__data += ("where {parameter} > {value}; ".format(parameter=parameter, value=value)
                            if value else '')

    def get_game(self, game_id):
        self.__data = SHORT_DESCRIPTION_FIELDS + "where id={id};".format(id=game_id)
        return json.loads(requests.post(self.__api_url, headers=self.__query_header, data=self.__data).text)

    def get_games(self, filter_dict={}):
        self.__data = SHORT_DESCRIPTION_FIELDS

        for key in filter_dict:
            if key is "rating":
                self.set_parameter(key, filter_dict[key], '>')
            else:
                self.set_parameter(key, filter_dict[key])

        return json.loads(requests.post(self.__api_url, headers=self.__query_header, data=self.__data).text)


