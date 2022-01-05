# File name:
	# Tweet_Sentiment_Analysis.py
# Description:
	# generates sentiment analysis for tweets
# Names of group members:  
    # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# main.py
# Other modules the file import:
	# pandas, numpy, re, nltk, seaborn
    # matplotlib.pyplot
    # textblob, string
# Dependency files
    # data/merged/tweets/tweets_cleaned.csv
    # data/merged/tweets/negative_tweets.csv
    # data/merged/tweets/neutral_tweets.csv
    # data/merged/tweets/positive_tweets.csv
# Online resources
    # none

import nltk
nltk.download('vader_lexicon')
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import nltk
import re
import string
# from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer as CV
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# reads data
def prepare_data(choice):
    tweets_df = pd.read_csv("data/merged/tweets/tweets_cleaned.csv")
    tweets = tweets_df['tweet']
    tweets = tweets.drop_duplicates()
    tweets_df = pd.DataFrame(tweets)
    # precomputed this to save you time (20 minutes) :)
    # compute_sentiment()
    negative_df = pd.read_csv("data/merged/tweets/negative_tweets.csv")
    neutral_df = pd.read_csv("data/merged/tweets/neutral_tweets.csv")
    positive_df = pd.read_csv("data/merged/tweets/positive_tweets.csv")
    if choice == 0:
        return positive_df
    elif choice == 1:
        return neutral_df
    else:
        return negative_df

#computes sentiments of tweets
def compute_sentiment():
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    polarity = 0
    neutral_tweets = []
    negative_tweets = []
    positive_tweets = []

    tweets_df = pd.read_csv("data/merged/tweets/tweets_cleaned.csv")
    tweets = tweets_df['tweet']
    tweets = tweets.drop_duplicates()

    for tweet in tweets:

        analysis = TextBlob(tweet)

        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']

        polarity += analysis.sentiment.polarity

        if neg > pos:
            negative_tweets.append(tweet)
            negative_count += 1
        elif pos > neg:
            positive_tweets.append(tweet)
            positive_count += 1
        elif pos == neg:
            neutral_tweets.append(tweet)
            neutral_count += 1

    tweets_df = pd.DataFrame(tweets)
    neutral_df = pd.DataFrame(neutral_tweets, columns=['tweet'])
    negative_df = pd.DataFrame(negative_tweets, columns=['tweet'])
    positive_df = pd.DataFrame(positive_tweets, columns=['tweet'])

    neutral_df.to_csv("data/merged/tweets/neutral_tweets.csv")
    positive_df.to_csv("data/merged/tweets/positive_tweets.csv")
    negative_df.to_csv("data/merged/tweets/negative_tweets.csv")

#generates plot_distribution
def plot_distribution(lst,title):
    plt.figure(figsize=(16,8))
    sns.kdeplot(lst,color="blue",label="Tweet")
    plt.title(title)
    plt.show()

# generates top n words
def get_top_n_words(corpus, n=None):
    vec = CV().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

# generates to bigram
def get_top_n_bigram(corpus, n=None):
    vec = CV(ngram_range=(2, 2)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

# generates a trigram
def get_top_n_trigram(corpus, n=None):
    vec = CV(ngram_range=(3, 3)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

# generates a plot 
def plot_bt(data,x,w,p, sentiment):
    common_words = x(data['tweet'], 20)
    common_words_df = pd.DataFrame (common_words,columns=['word','freq'])

    plt.figure(figsize=(16,8))
    sns.barplot(x='freq', y='word', data=common_words_df,facecolor=(0, 0, 0, 0),linewidth=3,edgecolor=sns.color_palette(p,20))
    plt.title("Top 20 "+ w + sentiment)
    plt.xlabel("Frequency", fontsize=14)
    plt.yticks(fontsize=13)
    plt.xticks(rotation=45, fontsize=13)
    plt.ylabel("")
    plt.show()
    return common_words_df

#generates a plot chart
def plot_charts(data, sentiment):
    text_len = data['tweet'].str.len()
    plot_distribution(text_len,"Character count distribution"+sentiment)


    common_words = get_top_n_words(data['tweet'], 20)
    common_words_df1 = pd.DataFrame(common_words,columns=['word','freq'])
    plt.figure(figsize=(16, 8))
    ax = sns.barplot(x='freq', y='word', data=common_words_df1,facecolor=(0, 0, 0, 0),linewidth=3,edgecolor=sns.color_palette("ch:start=3, rot=.1",20))

    plt.title("Top 20 unigrams" + sentiment)
    plt.xlabel("Frequency", fontsize=14)
    plt.yticks(fontsize=13)
    plt.xticks(rotation=45, fontsize=13)
    plt.ylabel("")
    plt.show()

    common_words_df2 = plot_bt(data,get_top_n_bigram,"bigrams","ch:rot=-.5",sentiment)
    common_words_df3 = plot_bt(data,get_top_n_trigram,"trigrams","ch:start=-1, rot=-.6", sentiment)

# shows positive tweets
def positiveTweets():
    plot_charts(prepare_data(0), " : Positive Tweets")

#shows neutral tweets
def neutralTweets():
    plot_charts(prepare_data(1), " : Neutral Tweets")

# shows positive tweets
def negativeTweets():
    plot_charts(prepare_data(2), " : Negative Tweets")
