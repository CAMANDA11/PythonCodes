# -*- coding: utf-8 -*-
"""Twitter API.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Zzi7kUNHqP0hZpgP2yLhNrubrFSWCrUT
"""

from google.colab import drive
drive.mount('/content/drive')

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 21:01:05 2021

@author: amand
"""

from textblob import TextBlob
from wordcloud import WordCloud
import tweepy
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
pio.renderers.default = "browser"

consumer_key = 'ZJIWDMcdyQICXHyXvaiY964SI'
consumer_key_secret = 'Holn2v1FsvZ7X8pwJium0X8U1WyhgKAyoBt98QfHvGatcr25CE'

access_token = '422571375-BPtrCfPeNQNlABfhAvBkLCCd2qRav8tQJvKD06q6'
access_token_secret = 'TlQP7UoT3Hx6CP2RPXAEriuHZXuZ2gQlKdt2Aw1JUGAPu'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


public_tweets = api.search('inflation in Nigeria')
tweet_amount= 1000
#tweets= tweepy.Cursor(api.search,q=public_tweets,lang='en', tweet_mode="extended")
tweets= tweepy.Cursor(api.search,q=public_tweets,lang='en',since ="2021-03-01", tweet_mode="extended").items(tweet_amount)

#for tweet in public_tweets:
#	print(tweet.text)
#	analysis = TextBlob(tweet.text)
#	print(analysis.sentiment)
#	if analysis.sentiment[0]>0:
#		print ('Positive')
#	else:
#		print ('Negative')
#	print("")