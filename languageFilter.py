import os
import pandas as pd
from textblob import TextBlob
import numpy as np
from datetime import datetime
from time import sleep

pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
df = pd.read_pickle("classified_tweet.pkl")

pd.set_option('display.max_colwidth', -1)

print ("Pickle file loaded from memory.")
print("Complete tweet data set size: ", df.shape)

neutral_tweet = df.loc[(df['vader_score'] == 'Neutral') & (df['textblob_score'] == 'Neutral') & (df['afinn_score'] == 'Neutral')]
non_neutral_tweet = df.loc[~((df['vader_score'] == 'Neutral') & (df['textblob_score'] == 'Neutral') & (df['afinn_score'] == 'Neutral'))]

print ("Language filter is being applied on", neutral_tweet.shape[0], "records.")

split_df = np.array_split(neutral_tweet, int(neutral_tweet.shape[0]/1000))

for idx, df_l in enumerate(split_df):
    print("Start time", datetime.now())
    df_l['lang'] = df_l.apply(lambda row: TextBlob(str(row.pre_proc)).detect_language() if len(str(row.pre_proc)) > 3 else '', axis=1)
    print("Chunk language detected, remaining ", len(split_df) - idx)
    print("End time", datetime.now())
    if (idx % 100) == 0:
        sleep(3600)
        continue
    sleep(2)

neutral_tweet = pd.concat(split_df, ignore_index=True)

print ("Extracted language.")

neutral_tweet = neutral_tweet.loc[neutral_tweet['lang'] == 'en']
print ("Applied filter on english language.")

df = pd.concat([neutral_tweet, non_neutral_tweet], ignore_index=True)

print ("Shape of tweets data frame after language filter,", df.shape)

df.to_pickle("lang_filter.pkl")

print ("Data language filter completed and saved to pickle file.")
