
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import nltk
import re
import time
import csv
import sys
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn import feature_extraction
from sklearn import metrics, svm, tree, ensemble, linear_model, naive_bayes
import textblob
import warnings
warnings.simplefilter('ignore')


# In[2]:

final = []
with open('reviews_60601-60606.csv') as csv_file:
    count = 0
    for line in csv.reader(csv_file):
        row = ','.join(line)
        rows = row.split(',') 
        rows[3:-6] = [''.join(rows[3:-6])]
        count += 1
        if len(rows) != 10:
            print(rows)
            sys.exit(1)
        final.append(rows)


# In[3]:

df = pd.DataFrame(final[1:])
df.columns = final[:1]

yelp_reviews = df.iloc[:,3:5]
ratings = yelp_reviews['rating'].values.tolist()
ratings = [int(x[0]) for x in ratings]


# In[4]:

labels = []

for i in range(len(ratings)):
	if ratings[i] == 1 or ratings[i] == 2 or ratings[i] ==  3:
		# negative
		labels.append(2)
	elif ratings[i] == 4 or ratings[i] == 5:
		# positive
		labels.append(1)

yelp_reviews['label'] = np.asarray(labels)
yelp_reviews.drop(['rating'], axis=1, inplace=True)


# In[5]:

def analyze_comment(cleaned_comments, label):
    """Analyze the cleaned comments."""
    polarity = []
    subjectivity = []
    sentiment = []
    for comment in cleaned_comments:
        comment = str(comment)
        polarity_comment = textblob.TextBlob(comment).sentiment.polarity
        subjectivity_comment = textblob.TextBlob(comment).sentiment.subjectivity
        polarity.append(polarity_comment)
        subjectivity.append(subjectivity_comment)
        if polarity_comment > 0.12:
            sentiment.append('positive')
        else:
            sentiment.append('negative')
    return cleaned_comments, label, np.asarray(polarity), np.asarray(subjectivity), np.asarray(sentiment)

cleaned_comments, label, polarity, subjectivity, sentiment = analyze_comment(np.asarray(yelp_reviews['reviewContent']), np.asarray(yelp_reviews['label']))


# In[6]:

yelp_analyzed = pd.DataFrame.from_dict({
                                'comment': cleaned_comments.reshape(cleaned_comments.shape[0]),
                                'label': label.reshape(label.shape[0]),
                                'sentiment' : sentiment.reshape(sentiment.shape[0]),
                                'subjectivity': subjectivity.reshape(subjectivity.shape[0]),
                                'polarity': polarity.reshape(polarity.shape[0])})


# In[7]:

yelp_analyzed['rating'] = ratings


# In[12]:

accScore = metrics.accuracy_score(yelp_analyzed['label'],[1 if x=='positive' else 2 for x in yelp_analyzed['sentiment'].tolist()])
print('Accuracy: ', accScore,'\n')
lbl = [1,2]
f1Score = metrics.f1_score(yelp_analyzed['label'],[1 if x=='positive' else 2 for x in yelp_analyzed['sentiment'].tolist()],average=None,labels=lbl)
for i in range(len(lbl)):
    print("F1-Score of %s class: %f" %(lbl[i],f1Score[i])) 


# In[15]:

average_positive_rating = yelp_analyzed.loc[yelp_analyzed['sentiment'] == 'positive']['rating'].sum()/yelp_analyzed.loc[yelp_analyzed['sentiment'] == 'positive'].shape[0]
average_negative_rating = yelp_analyzed.loc[yelp_analyzed['sentiment'] == 'negative']['rating'].sum()/yelp_analyzed.loc[yelp_analyzed['sentiment'] == 'negative'].shape[0]

print('\nAverage positive rating: ', average_positive_rating)
print('Average negative rating: ', average_negative_rating, '\n')


# In[16]:

yelp_analyzed['restaurantID'] = df['restaurantID']


# In[17]:

rest_data = pd.read_csv("restaurants_60601-60606.csv", usecols=[0,1])


# In[18]:

combined_yelp = pd.merge(yelp_analyzed, rest_data, left_on="restaurantID", right_on="restaurantID", how="left", validate="m:1")


# In[19]:

final_result = combined_yelp[['name', 'sentiment','rating']]


# In[20]:

final_result.to_csv('sentiment_analysis.csv', index=False)


# In[21]:

yelp_analyzed[['comment', 'sentiment', 'polarity', 'subjectivity', 'rating']].to_csv('sentiment_analysis_output.csv', index=False)


# In[ ]:



