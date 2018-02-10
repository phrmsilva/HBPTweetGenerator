import twitter
import os

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret = os.environ['CONSUMER_SECRET'],
        access_token_key = os.environ['ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET'])

DEFAULT_COUNT = 200

def get_tweets(user_name, count=DEFAULT_COUNT):
    tweets_text = [s.text.encode('ascii', 'ignore') for s in api.GetUserTimeline(include_rts=False,
                                                                                 screen_name=user_name)]

    if (count <= DEFAULT_COUNT):
        tweets_text = [s.text for s in api.GetUserTimeline(include_rts=False, screen_name=user_name)]
    else:
        tweets = api.GetUserTimeline(include_rts=True, screen_name=user_name)
        remaining = count - DEFAULT_COUNT
        last_tweet = tweets[-1].id
        tweets_text = [t.text for t in tweets]

        while remaining > 0:
            to_request = 0
            if remaining > 200:
                to_request = 200
                remaining -= 200
            else:
                to_request = remaining
                remaining = 0

        tweets = api.GetUserTimeline(include_rts=False, screen_name=user_name, count=to_request, max_id=last_tweet)
        if len(tweets) > 0:
            last_tweet = tweets[-1].id
        tweets_text += [t.text for t in tweets]
    return unicode_to_str(tweets_text)

def unicode_to_str(uc_list):
    return [s.encode('ascii', 'ignore') for s in uc_list]

def get_tweets_to_file(user_name, count=DEFAULT_COUNT, file_path=None):
    if file_path is None:
        file_path = './resources/' + user_name + '.txt'
    f = open(file_path, 'w')
    for t in get_tweets(user_name, count):
        f.write(t + '\n')
    f.close()
