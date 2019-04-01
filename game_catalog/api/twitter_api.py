import json

import requests
import six
from django.conf import settings
from requests_oauthlib import OAuth1


class TwitterApi:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):

        if type(consumer_key) == six.text_type:
            consumer_key = consumer_key.encode('ascii')

        if type(consumer_secret) == six.text_type:
            consumer_secret = consumer_secret.encode('ascii')

        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
        self.__session = requests.Session()
        self.__url = "https://api.twitter.com/1.1/search/tweets.json"

        self.__auth = OAuth1(self.__consumer_key,
                             client_secret=self.__consumer_secret,
                             resource_owner_key=self.__access_token,
                             resource_owner_secret=self.__access_token_secret,
                             decoding=None)

    def search(self, game):
        self.__session.params = {'q': game, "tweet_mode": "extended"}

        response = self.__session.request("GET", self.__url, auth=self.__auth)

        return json.loads(response.text)['statuses'] if response.status_code is settings.SUCCESS_STATUS else None
