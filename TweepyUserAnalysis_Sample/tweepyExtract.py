import tweepy
import os
import pickle

os.chdir("metoo_data")

key = "zISczi3xIqgOTW3C39MkgvoKp"
secret_key = "NFdOI9xynBWOSuBi5zbypXarhC8jjTKBkSy8NKo1yoEjja2j2t"

auth = tweepy.AppAuthHandler(key, secret_key)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = []

print("Extracting query using tweepy having #MeToo.")
for tweet in tweepy.Cursor(api.search, q='#MeToo', lang='en', tweet_mode='extended').items(75000):
    tweets.append(tweet)

with open("tweets_2604.pkl", 'wb') as f:
    pickle.dump(tweets, f)

print("#MeToo tweets extracted are", len(tweets))
