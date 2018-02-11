import twitter
import os, json, time

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret = os.environ['CONSUMER_SECRET'],
        access_token_key = os.environ['ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET'],
        sleep_on_rate_limit=True)

DEFAULT_TWEET_COUNT = 200
DEFAULT_SEARCH_RESULTS = 5
MAX_USER_SEARCH = 100
DEFAULT_RESULT_TYPE = 'mixed'

BANDS = json.load(open('./bands.json'))

def get_tweets(user_name, retweets=True, count=DEFAULT_TWEET_COUNT):
    print 'Getting tweets...'
    all_tweets = []

    newest_tweet_set = api.GetUserTimeline(screen_name=user_name, include_rts=retweets, count=count)
    all_tweets.extend(newest_tweet_set)
    if len(all_tweets) > 0:
        oldest = all_tweets[-1]

        if count > DEFAULT_TWEET_COUNT:
            while len(newest_tweet_set) > 0:
                newest_tweet_set = api.GetUserTimeline(screen_name=user_name,
                    include_rts=retweets, count=count, max_id=(oldest.id-1))
                all_tweets.extend(newest_tweet_set)
                oldest = all_tweets[-1]

        print('Retrieved {} tweets from {} since {}'.format(len(all_tweets), user_name, oldest.created_at))
    return unicode_to_str(all_tweets)

def get_search_tweets(band_name, count, result_type, max_id=None):
    return api.GetSearch(term=band_name, count=count, result_type=result_type, max_id=max_id, lang='en')

def get_users_from_tweets(tweets, only_non_verified=True):
    if only_non_verified:
        return [t.user.screen_name for t in tweets if not t.user.verified]
    return [t.user.screen_name for t in tweets]

def get_users_from_search(band_name, count, result_type):
    tweets = api.GetSearch(term=band_name, count=MAX_USER_SEARCH, result_type=result_type)
    users = get_users_from_tweets(tweets)
    if len(users) > count:
        users = users[0:(count-1)]

    return users

def get_fan_tweets(band_name, count=DEFAULT_SEARCH_RESULTS, result_type=DEFAULT_RESULT_TYPE):
    fan_tweets = []
    users = get_users_from_search(band_name, count=count, result_type=result_type)
    for u in users:
        fan_tweets.append(get_tweets(u, False))
    return fan_tweets

def get_bands_tweets():
    f = open('./band_and_tweets.json', 'w')
    d = {}
    for band in BANDS:
        all_fan_tweets = []
        for l in get_fan_tweets(band):
            all_fan_tweets.extend(l)
        d[band] = all_fan_tweets
    f.write(json.dumps(d))
    f.close()

def gbt():
    get_bands_tweets()

def unicode_to_str(uc_list):
    return [s.text.encode('ascii', 'ignore') for s in uc_list]

def get_tweets_to_file(user_name, count=DEFAULT_TWEET_COUNT, file_path=None):
    if file_path is None:
        file_path = './' + user_name + '.txt'
    f = open(file_path, 'w')
    for t in get_tweets(user_name, count):
        f.write(t + '\n')
    f.close()
