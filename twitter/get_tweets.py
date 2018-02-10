import twitter
import os

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret = os.environ['CONSUMER_SECRET'],
        access_token_key = os.environ['ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET'])

DEFAULT_COUNT = 200

def get_tweets(user_name, retweets=True, count=DEFAULT_COUNT):
    print('Getting tweets...')
    all_tweets = []

    newest_tweet_set = api.GetUserTimeline(screen_name=user_name, include_rts=retweets, count=count)
    all_tweets.extend(newest_tweet_set)
    oldest = all_tweets[-1]

    while len(newest_tweet_set) > 0:
        newest_tweet_set = api.GetUserTimeline(screen_name=user_name, include_rts=retweets, count=count, max_id=(oldest.id-1))
        all_tweets.extend(newest_tweet_set)
        oldest = all_tweets[-1]

    print('Retrieved {} tweets from {} since {}'.format(len(all_tweets), user_name, oldest.created_at))
    return unicode_to_str(all_tweets)

def unicode_to_str(uc_list):
    return [s.text.encode('ascii', 'ignore') for s in uc_list]

def get_tweets_to_file(user_name, count=DEFAULT_COUNT, file_path=None):
    if file_path is None:
        file_path = './resources/' + user_name + '.txt'
    f = open(file_path, 'w')
    for t in get_tweets(user_name, count):
        f.write(t + '\n')
    f.close()
