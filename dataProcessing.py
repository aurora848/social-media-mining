import os
import re
import pandas as pd
import pickle as pkl
from langdetect import detect
import nltk

def detectLang(text):
    try:
        if detect(text) != 'en':
            return 'nen'
        return 'en'
    except:
        return 'nen'

os.chdir("metoo_data")
months = ['October', 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
dirMonths = os.listdir(os.getcwd())
tweets = []
print ("Processing #MeToo tweets for the months: ", ' '.join(dirMonths))

for month in months:
    if month in dirMonths:
        for file in os.listdir(month):
            if file.endswith(".pkl"):
                tweets.extend(pkl.load(open(month+'//'+file, "rb")))
print ("Completed loading the pickle files.")
print ("Number of records to be processed for #MeToo: ",len(tweets))

df = pd.DataFrame.from_dict(tweets)

df['post_user'] = df.apply (lambda row: str(row.username).split()[0],axis=1)
print ("Extracted only the tweet poster's user name.")

df['hash_tags'] = df.apply (lambda row: ' '.join(re.findall('(?<=# ).+?(?= )', str(row.text), re.DOTALL)),axis=1)
print ("Extracted all the hashtags from tweets.")

# This takes a loooooong time to run - optimize
# df['lang'] = df.apply(lambda row: detectLang(str(row.text)),axis=1)
# print ("Extracted language type.")

# filter on lang once optimized

stop_words = set(nltk.corpus.stopwords.words('english'))
df['stop_filter'] = df.apply(lambda row: ' '.join([word for word in nltk.tokenize.word_tokenize(str(row.text)) if not word in stop_words]),axis=1)
print ("Removed all stop words from tweets.")

porter = nltk.stem.porter.PorterStemmer()
df['stem_filter'] = df.apply(lambda row: ' '.join([porter.stem(word) for word in nltk.tokenize.word_tokenize(str(row.stop_filter))]),axis=1)
print ("Stemmed words in tweets.")
nltk.download('wordnet')
lemmatizer = nltk.stem.WordNetLemmatizer()
df['lemma_filter'] = df.apply(lambda row: ' '.join([lemmatizer.lemmatize(word) for word in nltk.tokenize.word_tokenize(str(row.stop_filter))]),axis=1)
print ("Lemmatized words in tweets.")

# print(df.columns)
# print (df.dtypes)

# df_columns: ['date', 'favorites', 'geo', 'hashtags', 'mentions', 'permalink', 'retweets', 'term', 'text', 'tweet_id', 'username']
