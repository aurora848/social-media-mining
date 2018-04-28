import pandas as pd
import pickle as pkl

pd.options.mode.chained_assignment = None

tweets = pd.read_pickle("metoo_data\cleansed_tweet_1.pkl")
print ("Completed loading the pickle files.")
print ("Number of records to be processed for #MeToo: ",tweets.shape)
pd.set_option('display.max_colwidth', -1)
print (tweets.columns)
print (tweets.head(n=5))

# print(df.columns)
# print (df.dtypes)

# df_columns: ['date', 'favorites', 'geo', 'hashtags', 'mentions', 'permalink', 'retweets', 'term', 'text', 'tweet_id', 'username']
