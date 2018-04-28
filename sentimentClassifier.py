import os
import pandas as pd
from afinn import Afinn
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from datetime import datetime

pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
df = pd.read_pickle("cleansed_tweet.pkl")

pd.set_option('display.max_colwidth', -1)

print ("Pickle file loaded from memory.")
print("Complete tweet data set size: ", df.shape)

tweet = df.drop_duplicates('lemma_filter', keep='first')
print("Duplicates removed tweets data set size: ", tweet.shape)

print ("Begin sentiment classification using afinn, textblob and vader.")

afinn = Afinn()
tweet['afinn_score'] = tweet.apply(lambda row: 'Neutral' if afinn.score(str(row.lemma_filter)) == 0 else 'Positive' if afinn.score(str(row.lemma_filter)) > 0 else 'Negative', axis=1)
print ("Tweet sentiment generated using afinn.")

tweet['textblob_score'] = tweet.apply(lambda row: 'Neutral' if TextBlob(str(row.lemma_filter)).sentiment.polarity == 0 else 'Positive' if TextBlob(str(row.lemma_filter)).sentiment.polarity > 0 else 'Negative', axis=1)
print ("Tweet sentiment generated using textblob.")

sid = SentimentIntensityAnalyzer()
tweet['vader_score'] = tweet.apply(lambda row: 'Neutral' if sid.polarity_scores(str(row.lemma_filter))['compound'] == 0 else 'Positive' if sid.polarity_scores(str(row.lemma_filter))['compound'] > 0 else 'Negative', axis=1)
tweet['vader_cmp'] = tweet.apply(lambda row: sid.polarity_scores(str(row.lemma_filter))['compound'], axis=1)
print ("Tweet sentiment generated using Vader.")

print("Complete tweet data set size: ", df.shape)
print("Tweet data set size after removing duplicates & language filter: ", tweet.shape)

tweet.to_pickle("classified_tweet.pkl")

print ("Data sentiment classification completed and saved to pickle file.")
