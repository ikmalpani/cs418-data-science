
# coding: utf-8

# In[2]:

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


# In[3]:

fileObject = open('pickels/clean_reviews','rb')  
cleaned_reviews = pickle.load(fileObject)

fileObject = open('pickels/ratings','rb')  
ratings = pickle.load(fileObject)


# In[4]:

X_train, X_test, y_train, y_test = train_test_split(cleaned_reviews, ratings, test_size=0.2, random_state=42)


# In[5]:

def vectorization(train,test):
    vec = feature_extraction.text.TfidfVectorizer(min_df = 0.00125, max_df = 0.7, sublinear_tf=True, use_idf=True, stop_words=u'english', analyzer= 'word', ngram_range=(1,5),lowercase=True)
    train_vectors = vec.fit_transform(train)
    test_vectors = vec.transform(test)
    return train_vectors,test_vectors


# In[6]:

X_train, X_test = vectorization(X_train, X_test)


# In[10]:

X_train = X_train.toarray()
sm = SMOTE(random_state=43)
X_train, y_train = sm.fit_sample(X_train, y_train)


# In[11]:

fileObject = open('pickels/X_train','wb')
pickle.dump(X_train, fileObject) 
fileObject.close()

fileObject = open('pickels/X_test','wb')
pickle.dump(X_test, fileObject) 
fileObject.close()

fileObject = open('pickels/y_train','wb')
pickle.dump(y_train, fileObject) 
fileObject.close()

fileObject = open('pickels/y_test','wb')
pickle.dump(y_test, fileObject) 
fileObject.close()


# In[ ]:



