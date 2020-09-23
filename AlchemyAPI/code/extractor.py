# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 19:34:45 2020

@author: erick
"""

import GetOldTweets3 as got
import pandas as pd

class Extractor:

    def __init__(self):

        #External variables
        self.username = None
        self.count = None

        #Internal variables
        self.df = None
        self.tweets_extracted = None
        self.filename = None

    def preprocessing(self):  
        self.df = self.df.loc[:,'Text']
        self.df = self.df.str.replace(r'([@#][\w_-]+)',' ')
        self.df = self.df.str.lstrip().str.rstrip()
        self.df = self.df.values
        self.df = ' '.join(self.df)
        return self

    def save_df(self):
        with open("twitter.txt", "w", encoding='utf8') as text_file:
            text_file.write(self.df)

    def generate_twitter_df(self, username, count):
        print(username)
        print(count)
        # Creation of query object
        tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                                .setMaxTweets(count)
        # Creation of list that contains all tweets
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        # Creating list of chosen tweet data
        user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        self.df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Text'])

        self.tweets_extracted = len(self.df)

        self.filename = f'{username}-{int(count/1000)}k-tweets.csv'

        # Converting dataframe to CSV
        self.df.to_csv(self.filename, sep=',')

        return self

                
