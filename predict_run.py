import predict
import get_tweets
import sys

username = sys.argv[1]
print 'Getting tweets for ' + username + '...'
get_tweets.get_tweets_to_file(username)
print 'Predicting results for ' + username + '...'
predict.predict(username)
