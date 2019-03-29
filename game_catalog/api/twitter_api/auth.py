import six
from requests_oauthlib import OAuth1Session


class TwitterAuth:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, callback=None):

        if type(consumer_key) == six.text_type:
            consumer_key = consumer_key.encode('ascii')

        if type(consumer_secret) == six.text_type:
            consumer_secret = consumer_secret.encode('ascii')

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.callback = callback

        self.oauth = OAuth1Session(consumer_key,
                                   client_secret=consumer_secret,
                                   callback_uri=self.callback)

