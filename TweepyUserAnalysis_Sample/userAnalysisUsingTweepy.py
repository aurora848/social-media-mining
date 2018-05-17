import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import re
import pickle
import os

os.chdir("metoo_data")

pd.options.mode.chained_assignment = None

with open('tweets.pkl', 'rb') as f:
    tweets = pickle.load(f)

# print(len(tweets))

pd.set_option('display.max_colwidth', -1)

tweets_df = pd.DataFrame()

tweets_df['text'] = [tweet.full_text for tweet in tweets]
tweets_df['text_retweet_count'] = [tweet.retweet_count for tweet in tweets]

tweets_df['retweet_bin'] = [0 if tweet.retweet_count == 0 else 1 if tweet.retweet_count > 0 and tweet.retweet_count <= 100 else 2 if tweet.retweet_count > 100 and tweet.retweet_count <= 10000 else 3 for tweet in tweets]

tweets_df['tweet_fav_count'] = [tweet.favorite_count for tweet in tweets]

tweets_df['mentions'] = [tweet.favorite_count for tweet in tweets]
tweets_df['hashtagsOrNot'] = [1 if len(tweet.entities['hashtags']) > 0 else 0 for tweet in tweets]
tweets_df['urlsOrNot'] = [1 if len(tweet.entities['urls']) > 0 else 0 for tweet in tweets]

tweets_df['post_user'] = [tweet.user.id for tweet in tweets]
tweets_df['user_name'] = [tweet.user.name for tweet in tweets]
tweets_df['active_since'] = [(datetime.now() - tweet.user.created_at).days for tweet in tweets]
tweets_df['followers_count'] = [tweet.user.followers_count for tweet in tweets]

tweets_df['followers_bin'] = [0 if tweet.user.followers_count == 0 else 1 if tweet.user.followers_count > 0 and tweet.user.followers_count <= 100 else 2 if tweet.user.followers_count > 100 and tweet.user.followers_count <= 10000 else 3 for tweet in tweets]

tweets_df['favourites_count'] = [tweet.user.favourites_count for tweet in tweets]
tweets_df['statuses_count'] = [tweet.user.statuses_count for tweet in tweets]
tweets_df['friends_count'] = [tweet.user.friends_count for tweet in tweets]

tweets_df['pre_proc'] = tweets_df.apply(lambda row: re.sub('(rt)', '',re.sub('(http|https|ftp)\S+(?=( |$))', '',re.sub('(?<=)# .+?(?=( |$))', '',re.sub('(?<=)@ .+?(?=( |$))', '',str(row.text).lower())))),axis=1)

# print (tweets_df['text_retweet_count'].max())
# print (tweets_df['text_retweet_count'].min())

#print(tweets_df.head(n=5))
os.chdir("..")

print("Processed data")
vector_cv = CountVectorizer(max_df=0.99, min_df=0.01, stop_words='english', lowercase=True)
vector_ti = TfidfVectorizer(lowercase=True, stop_words="english", max_df = 0.99, min_df = 0.01)
print("Initializes vectors")
tweets_tfidf = vector_ti.fit_transform(tweets_df['pre_proc'])
print("TF-IDF fit complete")
tweets_cv = vector_cv.fit_transform(tweets_df['pre_proc'])
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
#
tweets_df.to_pickle("tweepy_user_analysis.pkl")
print("User analysis completed and results saved to pickle file.")

logClassifier = linear_model.LogisticRegression(C=1)

scores = cross_val_score(logClassifier, tweets_tfidf, tweets_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
#
scores = cross_val_score(logClassifier, tweets_lda_trn, tweets_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

scores = cross_val_score(logClassifier, tweets_df[['active_since','followers_count','favourites_count','statuses_count','friends_count']], tweets_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

scores = cross_val_score(logClassifier, tweets_df[['followers_count']], tweets_df['retweet_bin'], cv=5)
print ("Cross Validation scores: ", scores)
#
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

temp = tweets_df.retweet_bin.value_counts()

temp_df = temp.to_frame()
temp_df['bin'] = temp_df.index
ax = temp_df.plot.scatter(x = 'bin', y = 'retweet_bin')
ax.set_xlabel("Retweet bin", fontsize=12)
ax.set_ylabel("Message count", fontsize=12)
plt.savefig('scatterplot.png', bbox_inches='tight')
