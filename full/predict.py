import json
import random
from string import punctuation

import tensorflow as tf
import tflearn as tfl
import nltk
import numpy

lstemmer = nltk.stem.lancaster.LancasterStemmer()

JUST_BANDS = './bands.json'

def import_json_data(filePath):
    return json.load(open(filePath))

def strip_punctuation(s):
    return str(s).translate(None, punctuation)

def generate_nn_model(for_training=True):
    bands = import_json_data('./bands.json')
    all_words = []
    documents = []

    for b in bands:
        band_tweets_data = import_json_data('../band_tweets/' + b + '.json')
        for tweet in band_tweets_data:
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
    # nn = tfl.fully_connected(nn, 8)
    nn = tfl.fully_connected(nn, len(train_bands[0]), activation='softmax')
    nn = tfl.regression(nn)

    # Setting up tensorboard, start training
    model = tfl.DNN(nn, tensorboard_dir='./tflearn/tflearn_logs')
    if for_training:
        return (model, train_tweets, train_bands)
    return (model, all_words)

def train():
    model, tt, tb = generate_nn_model()
    model.fit(tt, tb, n_epoch=1000, batch_size=8)
    model.save('tflearn/model.tflearn')
    print 'Done training the model'

def tensorflow_record(user, all_words):
    tweets_words = nltk.word_tokenize(open('./' + user + '.txt').read())
    stem_tweets_words = [lstemmer.stem(tw) for tw in tweets_words]
    doc_words = [0] * len(all_words)
    for stw in stem_tweets_words:
        for i, w in enumerate(all_words):
            if w == stw:
                doc_words[i] = 1

    return numpy.array(doc_words)

def predict(username):
    m, aw = generate_nn_model(for_training=False)
    m.load('tflearn/model.tflearn')

    tfr = tensorflow_record(username, aw)
    # m = model.load('model.tflearn')
    band_list = import_json_data('./bands.json')
    prediction_list = m.predict([tfr])[0]

    # print str(band_list)
    # print str(m.predict([tfr])[0])

    bands_and_probs = [(band_list[i], prediction_list[i]) for i in xrange(len(band_list))]
    bands_and_probs.sort(key=lambda x:x[1], reverse=True)

    print "Top 3 bands:"
    for i in xrange(3):
        print str(bands_and_probs[i][0]) + '\t' + str(bands_and_probs[i][1])

    # print str(bands_and_probs)
    # print str(import_json_data('./bands.json')[numpy.argmax(m.predict([tfr]))])

# train()
#predict('schrobiwan')
