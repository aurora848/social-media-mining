import os
import re
import pandas as pd
import pickle as pkl
import nltk
from nltk.corpus import wordnet


pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
months = ['October', 'November', 'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
dirMonths = os.listdir(os.getcwd())
tweets = []
print ("Processing #MeToo tweets for the months: ", ' '.join(dirMonths))

for month in months:
    if month in dirMonths:
        size = 0
        for file in os.listdir(month):
            if file.endswith(".pkl"):
                temp = pkl.load(open(month + '//' + file, "rb"))
                size += len(temp)
                for row in temp:
                    row['date'] = file.replace('_#metoo_tweets.pkl','')
                tweets.extend(temp)
        print("Loaded data for the month of ", month)
        print("Number of records during ", month, "is ", size)
print ("Completed loading the pickle files.")
print ("Number of records to be processed for #MeToo: ",len(tweets))
df = pd.DataFrame.from_dict(tweets)

df['post_user'] = df.apply (lambda row: str(row.username).split()[0],axis=1)
print ("Extracted only the tweet poster's user name.")

df['hashtags'] = df.apply (lambda row: ' '.join(re.findall('(?<=# ).+?(?= )', str(row.text), re.DOTALL)),axis=1)
print ("Extracted all the hashtags from tweets.")

df['mentions'] = df.apply (lambda row: ' '.join(re.findall('(?<=@ ).+?(?= )', str(row.text), re.DOTALL)),axis=1)
print ("Extracted all the mentions from tweets.")

df['pre_proc'] = df.apply(lambda row: re.sub('(rt)', '',re.sub('(http|https|ftp)\S+(?=( |$))', '',re.sub('(?<=)# .+?(?=( |$))', '',re.sub('(?<=)@ .+?(?=( |$))', '',str(row.text).lower())))),axis=1)
print ("Removed all hashtags, mentions, rt, url from tweets.")

stop_words = set(nltk.corpus.stopwords.words('english'))
df['stop_filter'] = df.apply(lambda row: ' '.join([word for word in nltk.tokenize.word_tokenize(str(row.pre_proc)) if not word in stop_words]),axis=1)
print ("Removed all stop words from tweets.")

#nltk.download('averaged_perceptron_tagger')
df['pos_tags'] = df.apply(lambda row: str(nltk.pos_tag(nltk.tokenize.word_tokenize(str(row.stop_filter)))),axis=1)
print ("Added parts of speech tagging.")

porter = nltk.stem.porter.PorterStemmer()
df['stem_filter'] = df.apply(lambda row: ' '.join([porter.stem(word) for word in nltk.tokenize.word_tokenize(str(row.stop_filter))]),axis=1)
print ("Stemmed words in tweets.")

#nltk.download('wordnet')
lemmatizer = nltk.stem.WordNetLemmatizer()
df['lemma_filter'] = df.apply(lambda row: ' '.join([lemmatizer.lemmatize(word) if (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None) is None else lemmatizer.lemmatize(word, (wordnet.ADJ if pos_tag.startswith('J') else wordnet.VERB if pos_tag.startswith('V') else wordnet.NOUN if pos_tag.startswith('N') else wordnet.ADV if pos_tag.startswith('R') else None)) for word, pos_tag in eval(row.pos_tags)]),axis=1)
print ("Lemmatized words in tweets.")

df.to_pickle("cleansed_tweet_1.pkl")

print ("Data cleansing completed and saved to pickle file.")
