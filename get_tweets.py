import twitter
import os

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret = os.environ['CONSUMER_SECRET'],
        access_token_key = os.environ['ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET'])

def get_tweets(user_name):
    return [s.text.encode('ascii', 'ignore') for s in api.GetUserTimeline(screen_name=user_name)]
