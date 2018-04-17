
# coding: utf-8

# In[3]:

import pandas as pd
import numpy as np
import nltk
import re
import time
import csv
import sys
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn import feature_extraction
from sklearn import metrics, svm, tree, ensemble, linear_model, naive_bayes
from sklearn.ensemble import VotingClassifier
import xgboost as xgb
import warnings; warnings.simplefilter('ignore')


# In[4]:

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


# In[5]:

df = pd.DataFrame(final[1:])
df.columns = final[:1]

yelp_reviews = df.iloc[:,3:5]

reviews = yelp_reviews['reviewContent'].values.tolist()
ratings = yelp_reviews['rating'].values.tolist()


# In[6]:

def dataClean(reviews_raw):
    cleanReviews = []
    for review in reviews_raw:
        review = review[0].lower() #convert to lowercase
        review = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', review) #remove URL
        review = re.sub(r'(\s)@\w+', r'', review) #remove usernames
        review = re.sub(r'@\w+', r'', review) #remove usernames
        review = re.sub('<[^<]+?>', '', review) #remove HTML tags
        review = re.sub(r'[<>!#@$:.,%\?-]+', r'', review) #remove punctuation and special characters 
        lower_case = review.lower() #tokenization 
        words = lower_case.split()
        review = ' '.join([w for w in words if not w in nltk.corpus.stopwords.words("english")]) #remove stopwords
        ps = nltk.stem.PorterStemmer()
        stemmedReview = [ps.stem(word) for word in review.split(" ")]
        stemmedReview = " ".join(stemmedReview)
        review = str(stemmedReview)
        review = review.replace("'", "")
        review = review.replace("\"","")
        cleanReviews.append(review)
    return cleanReviews


# In[ ]:

cleaned_reviews = dataClean(reviews)


# In[ ]:

cleaned_reviews


# In[10]:

fileObject = open('pickels/clean_reviews','wb')
pickle.dump(cleaned_reviews, fileObject) 
fileObject.close()

fileObject = open('pickels/ratings','wb')
pickle.dump(ratings, fileObject) 
fileObject.close()


# In[ ]:



