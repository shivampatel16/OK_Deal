#!/usr/bin/env python3

# File name:
	# clean_tweets.py
# Description:
	# formats phonearena specifications extrated csv file. cleans it
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
    # pandas , re
# Dependency files
    # data/merged/tweets/tweets_merged_not_cleaned.csv
    # data/merged/tweets/tweets_cleaned.csv

# imports
import pandas as pd
import re
import os

# function to clean tweets
def clean_tweets():
    os.chdir('..')
    os.chdir('..')
    df = pd.read_csv("data/tweets/tweets_merged_not_cleaned.csv")
    os.remove("data/tweets/tweets_merged_not_cleaned.csv")
    df.to_csv("data/merged/tweets/tweets_merged_not_cleaned.csv")
    df = df[['phone name','date','username', 'tweet', 'language', 'replies_count', 'retweets_count', 'likes_count',
        'hashtags', 'link']]

    print("Filtering English tweets...")
    df = df[df["language"] == "en"]
    df.reset_index(drop=True, inplace=True)

    def get_tweet_text(tweet):
        #remove urls
        tweet = re.sub(r"http\S+", "", tweet) 
        tweet = re.sub(r'\S+\.com\S+','',tweet) 
        
        #remove mentions
        tweet = re.sub(r'\@\w+','',tweet) 
        
        #remove hashtags
        tweet = re.sub(r'\#\w+','',tweet) 
        
        return tweet

    print("Cleaning tweets...")
    df['tweet']=df['tweet'].apply(lambda x: get_tweet_text(x))
    print("Cleaning tweets completed...")

    df.to_csv("data/merged/tweets/tweets_cleaned.csv")
    


# clean_tweets()