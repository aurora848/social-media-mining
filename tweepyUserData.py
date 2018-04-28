import os
import pandas as pd
import tweepy
import datetime

key = "zISczi3xIqgOTW3C39MkgvoKp"
secret_key = "NFdOI9xynBWOSuBi5zbypXarhC8jjTKBkSy8NKo1yoEjja2j2t"

auth = tweepy.AppAuthHandler(key, secret_key)

pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
df = pd.read_pickle("cleansed_tweet_user.pkl")
print(df.columns)
pd.set_option('display.max_colwidth', -1)

print ("Pickle file loaded from memory.")
print("Complete tweet data set size: ", df.shape)

tweet = df.drop_duplicates("lemma_filter", keep='first')
print("Tweet data set size after removing duplicates: ", tweet.shape)

user_unique = tweet.post_user.unique()
print ("Unique users in the dataset are ", user_unique.shape)

user_tweet = tweet.groupby('post_user')['pre_proc'].apply(' '.join).reset_index()
print ("Tweets grouped by users shape ", user_tweet.shape)

for i, row in user_tweet.iterrows():
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        user_account = api.get_user(str(row['post_user']))
    except Exception as e:
        user_tweet['followers_count'] = -1
        user_tweet['statuses_count'] = -1
        user_tweet['friends_count'] = -1
        user_tweet['active_since'] = -1
        continue
    else:
        user_tweet['followers_count'] = user_account.followers_count
        user_tweet['statuses_count'] = user_account.statuses_count
        user_tweet['friends_count'] = user_account.friends_count
        user_tweet['active_since'] = (datetime.datetime.now() - user_account.created_at).days

print ("Extracted users followers, tweets, following and active since days.")

user_tweet.to_pickle("tweepy_user_analysis.pkl")
print ("User analysis completed and results saved to pickle file.")
