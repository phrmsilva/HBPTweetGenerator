import json
import random
from string import punctuation

import tensorflow as tf
import tflearn as tfl
import nltk
import numpy

lstemmer = nltk.stem.lancaster.LancasterStemmer()

JUST_BANDS = './bands.json'
BANDS_AND_TWEETS = './search_data.json'

def import_json_data(filePath):
    return json.load(open(filePath))

def strip_punctuation(s):
    return str(s).translate(None, punctuation)

def train(username):

    band_tweets_data = import_json_data('./bandstweets.json')
    bands = list(band_tweets_data.keys())
    all_words = []
    documents = []

    for b in bands:
        for tweet in band_tweets_data[b]:
            clean_tweet = strip_punctuation(tweet)
            twords = nltk.word_tokenize(clean_tweet)
            all_words += twords
            documents.append((twords, b))

    all_words = [lstemmer.stem(w.lower()) for w in all_words]
    all_words = list(set(all_words)) # removes duplicates

    training = []

    for doc in documents:
        doc_words = []
        token_words = doc[0]
        token_words = [lstemmer.stem(tw.lower()) for tw in token_words]

        for w in all_words:
            if w in token_words:
                doc_words.append(1)
            else:
                doc_words.append(0)

        output_row = [0] * len(bands)
        output_row[bands.index(doc[1])] = 1

        training.append([doc_words, output_row])

    random.shuffle(training)
    nptraining = numpy.array(training)

    train_tweets = list(nptraining[:, 0])
    train_bands = list(nptraining[:, 1])

    # Build neural network
    tf.reset_default_graph()
    nn = tfl.input_data(shape=[None, len(train_tweets[0])])
    nn = tfl.fully_connected(nn, 8)
    nn = tfl.fully_connected(nn, 8)
    nn = tfl.fully_connected(nn, len(train_bands[0]), activation='softmax')
    nn = tfl.regression(nn)

    # Setting up tensorboard, start training
    model = tfl.DNN(nn, tensorboard_dir='./tflearn/tflearn_logs')
    model.fit(train_tweets, train_bands, n_epoch=1000, batch_size=8)
    model.save('tflearn/model.tflearn')

    eval(username, model, all_words)

def tensorflow_record(user, all_words):
    tweets_words = nltk.word_tokenize(open('./user.txt').read())
    stem_tweets_words = [lstemmer.stem(tw) for tw in tweets_words]
    doc_words = [0] * len(all_words)
    for stw in stem_tweets_words:
        for i, w in enumerate(all_words):
            if w == stw:
                doc_words[i] = 1

    return numpy.array(doc_words)

def eval(username, m, all_words):
    tfr = tensorflow_record(username, all_words)
    # m = model.load('model.tflearn')
    print str(import_json_data('./bandstweets.json').keys()[numpy.argmax(m.predict([tfr]))])

train()
