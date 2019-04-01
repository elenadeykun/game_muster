import json
from datetime import datetime

import requests
import six
from django.conf import settings
from requests_oauthlib import OAuth1


class TwitterApi:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.__session = requests.Session()
        self.__url = "https://api.twitter.com/1.1/search/tweets.json"

        self.__auth = OAuth1(consumer_key,
                             client_secret=consumer_secret,
                             resource_owner_key=access_token,
                             resource_owner_secret=access_token_secret,
                             decoding=None)

    @staticmethod
    def __get_request_dict(response):
        tweets = json.loads(response.text)['statuses']
        tweets_dict = []
        if tweets:
            for tweet in tweets:
                (tweets_dict.append({'text': tweet['full_text'], 'user': tweet['user']['screen_name'],
                 'date': datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')}))

        return tweets_dict

    def search(self, game):
        self.__session.params = {'q': game, "tweet_mode": "extended"}

        response = self.__session.request("GET", self.__url, auth=self.__auth)

        return self.__get_request_dict(response) if response.status_code is settings.SUCCESS_STATUS else None
