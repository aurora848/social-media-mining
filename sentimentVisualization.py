import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import math

pd.options.mode.chained_assignment = None

os.chdir("metoo_data")
df = pd.read_pickle("classified_tweet.pkl")
print ("Pickle file loaded from memory.")
pd.set_option('display.max_colwidth', -1)

visual_bin_df = pd.DataFrame(columns=['bin_num', 'pos_count', 'neg_count', 'neu_count', 'subjectivity', 'polarity', 'subj_log2', 'pol_log2'])
visual_con_df = pd.DataFrame(columns=['bin_num', 'pos_count', 'neg_count', 'neu_count', 'subjectivity', 'polarity', 'subj_log2', 'pol_log2'])

date_unique = df.date.unique()
bin_num = 1

df['bin_num'] = 0
df['con_bin'] = 0
pd.set_option('display.max_colwidth', -1)
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

for counter, in_date in enumerate(date_unique):
    cnv_date = datetime.strptime(in_date, "%Y-%m-%d")
    if (cnv_date.weekday()) == 6 and  counter != 0:
        bin_num += 1
    if (cnv_date.weekday()) < 4:
        df.loc[(df.date == cnv_date), 'con_bin'] = bin_num
    if (cnv_date.weekday()) > 3:
        df.loc[(df.date == cnv_date), 'con_bin'] = bin_num + 1
    df.loc[(df.date == cnv_date), 'bin_num'] = bin_num

bin_unique = df.bin_num.unique()

print ("Number of bins for visualizations are ", len(bin_unique))

for in_bin in sorted(bin_unique):
    temp_pos = df.loc[(df['bin_num'] == in_bin) & (df['vader_score'] == 'Positive')]
    temp_neg = df.loc[(df['bin_num'] == in_bin) & (df['vader_score'] == 'Negative')]
    temp_neu = df.loc[(df['bin_num'] == in_bin) & (df['vader_score'] == 'Neutral')]
    subj = (temp_pos.shape[0] + temp_neg.shape[0]) / temp_neu.shape[0]
    pol = temp_pos.shape[0] / temp_neg.shape[0]
    visual_bin_df = visual_bin_df.append({'bin_num': in_bin, 'pos_count': temp_pos.shape[0], 'neg_count': temp_neg.shape[0], 'neu_count': temp_neu.shape[0], 'subjectivity': subj, 'polarity': pol, 'subj_log2': math.log(subj,2), 'pol_log2':math.log(pol,2)}, ignore_index=True)
    temp_pos = df.loc[(df['con_bin'] == in_bin) & (df['vader_score'] == 'Positive')]
    temp_neg = df.loc[(df['con_bin'] == in_bin) & (df['vader_score'] == 'Negative')]
    temp_neu = df.loc[(df['con_bin'] == in_bin) & (df['vader_score'] == 'Neutral')]
    subj = (temp_pos.shape[0] + temp_neg.shape[0]) / temp_neu.shape[0]
    pol = temp_pos.shape[0] / temp_neg.shape[0]
    visual_con_df = visual_con_df.append({'bin_num': in_bin, 'pos_count': temp_pos.shape[0], 'neg_count': temp_neg.shape[0], 'neu_count': temp_neu.shape[0], 'subjectivity': subj, 'polarity': pol, 'subj_log2': math.log(subj,2), 'pol_log2':math.log(pol,2)}, ignore_index=True)

#print ("Dates for visualizations\n",'\n'.join(date_unique))
#print ("Bins for visualizations\n", bin_unique)

print ("Data subjectivity and polarity calculation completed.")

df_vader = df[['vader_score', 'vader_cmp', 'bin_num']]
df_den = df[['vader_cmp']]
df_den_bin = df[['vader_cmp', 'bin_num', 'con_bin']]

del df['favorites']
del df['geo']
del df['hashtags']
del df['mentions']
del df['permalink']
del df['term']
del df['retweets']
del df['text']
del df['tweet_id']
del df['username']
del df['post_user']
del df['pre_proc']
del df['stop_filter']
del df['pos_tags']
del df['stem_filter']
del df['lemma_filter']
del df['afinn_score']
del df['textblob_score']

df.to_csv('classified_sent.csv', encoding='utf-8')
visual_con_df.to_csv('visual_cont_bin.csv', encoding='utf-8')
visual_bin_df.to_csv('visual_week_bin.csv', encoding='utf-8')
print("Subjectivity & Polarity scores saved to file.")

sns.distplot(df_den['vader_cmp'])
plt.savefig('Vader_Cmd_kde_Dist.png', bbox_inches='tight')
print("Vader kde plot completed.")

ax = visual_bin_df.plot(y = 'subj_log2', x = 'bin_num', kind='bar', title ="Subjectivity", figsize=(15, 10), fontsize=12)
ax.set_xlabel("Weekly bin", fontsize=12)
ax.set_ylabel("Subjectivity Weekly score", fontsize=12)
#plt.show()
plt.savefig('subjectivity_week_bar.png', bbox_inches='tight')
print("Subjectivity bar chart plot completed for weekly bin.")

ax = visual_bin_df.plot(y = 'pol_log2', x = 'bin_num', kind='bar', title ="Polarity", figsize=(15, 10), fontsize=12)
ax.set_xlabel("Weekly bin", fontsize=12)
ax.set_ylabel("Polarity Weekly score", fontsize=12)
#plt.show()
plt.savefig('polarity_week_bar.png', bbox_inches='tight')
print("Polarity bar chart plot completed for weekly bin.")

ax = visual_con_df.plot(y = 'subj_log2', x = 'bin_num', kind='bar', title ="Subjectivity", figsize=(15, 10), fontsize=12)
ax.set_xlabel("Weekly Continuous bin", fontsize=12)
ax.set_ylabel("Subjectivity score", fontsize=12)
#plt.show()
plt.savefig('subjectivity_cont_bar.png', bbox_inches='tight')
print("Subjectivity bar chart plot completed for continuous bin.")

ax = visual_con_df.plot(y = 'pol_log2', x = 'bin_num', kind='bar', title ="Polarity", figsize=(15, 10), fontsize=12)
ax.set_xlabel("Weekly Continuous bin", fontsize=12)
ax.set_ylabel("Polarity score", fontsize=12)
#plt.show()
plt.savefig('polarity_cont_bar.png', bbox_inches='tight')
print("Polarity bar chart plot completed for continuous bin.")

ax = df_vader.boxplot(column = ['vader_cmp'], by = 'vader_score')
ax.set_xlabel("Vader compound value", fontsize=12)
#plt.show()
plt.savefig('Vader_Boxplot_Score.png', bbox_inches='tight')

ax = df_vader.boxplot(column = ['vader_cmp'], by = 'bin_num')
ax.set_xlabel("Vader compound value", fontsize=12)
#plt.show()
plt.savefig('Vader_Boxplot_Bins.png', bbox_inches='tight')

print("Vader box plot completed.")
