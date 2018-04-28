import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from textblob import TextBlob
from time import sleep
from datetime import datetime
import nltk

pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
df = pd.read_pickle("cleansed_tweet.pkl")
pd.set_option('display.max_colwidth', -1)

print ("Pickle file loaded from memory.")
print("Complete tweet data set size: ", df.shape)

tweet = df.drop_duplicates("lemma_filter", keep='first')
print("Tweet data set size after removing duplicates: ", tweet.shape)

user_unique = tweet.post_user.unique()
print ("Unique users in the dataset are ", user_unique.shape)

user_tweet = tweet.groupby('post_user')['pre_proc'].apply(' '.join).reset_index()
print ("Tweets grouped by users shape ", user_tweet.shape)
# print(user_tweet.columns)

user_param = tweet.groupby('post_user')['favorites', 'retweets'].sum().reset_index()
print ("Favorite & Retweet grouped by users shape ", user_param.shape)
# print(user_param.columns)

user_df = pd.merge(user_tweet, user_param, on = 'post_user')
print ("Merged user dataframe's shape ", user_param.shape)

vector_cv = CountVectorizer(max_df=0.99, min_df=0.01, stop_words='english', lowercase=True)
vector_ti = TfidfVectorizer(lowercase=True, stop_words="english", max_df = 0.99, min_df = 0.01)

tweets_tfidf = vector.fit_transform(tweets['pre_proc'])

tweets_cv = vector_cv.fit_transform(tweets['pre_proc'])
feature_names = vector_cv.get_feature_names()

no_topics = 10

lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50, random_state=0, n_jobs=4)
tweets_lda = lda.fit(tweets_cv)
tweets_lda_trn = lda.transform(tweets_cv)

user_df.to_pickle("user_analysis.pkl")
print ("User analysis completed and results saved to pickle file.")
