
# coding: utf-8

# In[1]:

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
from sklearn import feature_extraction, model_selection
from sklearn import metrics, svm, tree, ensemble, linear_model, naive_bayes
from sklearn.ensemble import VotingClassifier
import xgboost as xgb
import warnings; warnings.simplefilter('ignore')


# In[2]:

fileObject = open('pickels/X_train','rb')  
X_train = pickle.load(fileObject)

fileObject = open('pickels/y_train','rb')  
y_train = pickle.load(fileObject)

fileObject = open('pickels/X_test','rb')  
X_test = pickle.load(fileObject)

fileObject = open('pickels/y_test','rb')  
y_test = pickle.load(fileObject)


# In[3]:

y_test = [int(item) for items in y_test for item in items]


# In[4]:

X = np.vstack((X_train, X_test.toarray()))


# In[5]:

Y = y_train.tolist() + y_test


# In[6]:

clfs = [naive_bayes.BernoulliNB(),svm.SVC(kernel='rbf', gamma=0.58, C=0.81),tree.DecisionTreeClassifier(random_state=0),ensemble.RandomForestClassifier(criterion='entropy', n_jobs = 10),linear_model.LogisticRegression(),linear_model.SGDClassifier(),ensemble.GradientBoostingClassifier(),xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)]


# In[9]:

for clf in clfs:
    clf.fit(X, Y)
    preds = model_selection.cross_val_predict(clf, X, Y, cv=10)
    accScore = metrics.accuracy_score(Y,preds)

    lbl = [1,2,3,4,5]
    precision = metrics.precision_score(Y,preds,average=None,labels=lbl)
    recall = metrics.recall_score(Y,preds,average=None,labels=lbl)
    f1Score = metrics.f1_score(Y,preds,average=None,labels=lbl)
    
    print(clf);
    print("\nOverall Acurracy: ",accScore,"\n")

    for i in range(len(lbl)):
        print("Precision of %s class: %f" %(lbl[i],precision[i]))
        print("Recall of %s class: %f" %(lbl[i],recall[i]))
        print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[ ]:

eclf = VotingClassifier(estimators=[('bnb', clfs[0]), ('svm', clfs[1]),('dt', clfs[2]), ('rf', clfs[3]),('lr',clfs[4]),('sgd',clfs[5]),('gb',clfs[6])], voting='hard') # ,('xgb',clfs[7])
clf.fit(X, Y)
preds = model_selection.cross_val_predict(clf, X, Y, cv=10)
accScore = metrics.accuracy_score(Y,preds)

lbl = [1,2,3,4,5]
precision = metrics.precision_score(Y,preds,average=None,labels=lbl)
recall = metrics.recall_score(Y,preds,average=None,labels=lbl)
f1Score = metrics.f1_score(Y,preds,average=None,labels=lbl)

print(clf);
print("\nOverall Acurracy: ",accScore,"\n")

for i in range(len(lbl)):
    print("Precision of %s class: %f" %(lbl[i],precision[i]))
    print("Recall of %s class: %f" %(lbl[i],recall[i]))
    print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[ ]:



