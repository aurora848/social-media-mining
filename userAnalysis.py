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

user_df['retweet_bin'] = df.apply(lambda row: 0 if int(row.text) == 0 else 1 if int(row.text) > 0 and int(row.text) <= 100 else 2 if int(row.text) > 100 and int(row.text) <= 10000 else 3, axis=1)

os.chdir("..")

print("Processed data")
vector_cv = CountVectorizer(max_df=0.99, min_df=0.01, stop_words='english', lowercase=True)
vector_ti = TfidfVectorizer(lowercase=True, stop_words="english", max_df = 0.99, min_df = 0.01)
print("Initializes vectors")
tweets_tfidf = vector_ti.fit_transform(user_df['pre_proc'])
print("TF-IDF fit complete")
tweets_cv = vector_cv.fit_transform(user_df['pre_proc'])
print("CV fit complete")
feature_names = vector_cv.get_feature_names()
#
no_topics = 10
#
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50, random_state=0)
tweets_lda = lda.fit(tweets_cv)
print("LDA fit complete")
#
tweets_lda_trn = lda.transform(tweets_cv)
print("LDA transform complete")

logClassifier = linear_model.LogisticRegression(C=1)

scores = cross_val_score(logClassifier, tweets_tfidf, user_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#
scores = cross_val_score(logClassifier, tweets_lda_trn, user_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

scores = cross_val_score(logClassifier, user_df[['active_since','followers_count','favourites_count','statuses_count','friends_count']], tweets_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

scores = cross_val_score(logClassifier, user_df[['followers_count']], user_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

temp = user_df.retweet_bin.value_counts()

temp_df = temp.to_frame()
temp_df['bin'] = temp_df.index
ax = temp_df.plot.scatter(x = 'bin', y = 'retweet_bin')
ax.set_xlabel("Retweet bin", fontsize=12)
ax.set_ylabel("Message count", fontsize=12)
plt.savefig('scatterplot.png', bbox_inches='tight')
