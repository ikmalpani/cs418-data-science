
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
from sklearn import feature_extraction
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


# In[4]:

clfs = [naive_bayes.BernoulliNB(),svm.SVC(kernel='rbf', gamma=0.58, C=0.81),tree.DecisionTreeClassifier(random_state=0),ensemble.RandomForestClassifier(criterion='entropy', n_jobs = 10),linear_model.LogisticRegression(),linear_model.SGDClassifier(),ensemble.GradientBoostingClassifier()]


# In[ ]:

for clf in clfs:
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test.toarray())
    accScore = metrics.accuracy_score(y_test,preds)

    lbl = [1,2,3,4,5]
    precision = metrics.precision_score(y_test,preds,average=None,labels=lbl)
    recall = metrics.recall_score(y_test,preds,average=None,labels=lbl)
    f1Score = metrics.f1_score(y_test,preds,average=None,labels=lbl)
    
    print(clf);
    print("\nOverall Acurracy: ",accScore,"\n")

    for i in range(len(lbl)):
        print("Precision of %s class: %f" %(lbl[i],precision[i]))
        print("Recall of %s class: %f" %(lbl[i],recall[i]))
        print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[5]:

eclf = VotingClassifier(estimators=[('bnb', clfs[0]), ('dt', clfs[1]), ('rf', clfs[2]),('lr',clfs[3]),('sgd',clfs[4]),('gb',clfs[5])], voting='hard')
eclf.fit(X_train, y_train)
preds = eclf.predict(X_test.toarray())
accScore = metrics.accuracy_score(y_test,preds)
labels = [1,2,3,4,5]

precision = metrics.precision_score(y_test,preds,average=None,labels=labels)
recall = metrics.recall_score(y_test,preds,average=None,labels=labels)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=labels)

print(eclf)
print("\nOverall Acurracy: ",accScore,"\n")

for i in range(len(labels)):
    print("Precision of %s class: %f" %(labels[i],precision[i]))
    print("Recall of %s class: %f" %(labels[i],recall[i]))
    print("F1-Score of %s class: %f" %(labels[i],f1Score[i]),"\n")


# In[6]:




# In[ ]:

clf = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
clf.fit(X_train, y_train)
preds = clf.predict(X_test.toarray())
accScore = metrics.accuracy_score(y_test,preds)
labels = [1,2,3,4,5]

precision = metrics.precision_score(y_test,preds,average=None,labels=labels)
recall = metrics.recall_score(y_test,preds,average=None,labels=labels)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=labels)

print(clf)
print("\nOverall Acurracy: ",accScore,"\n")

for i in range(len(labels)):
    print("Precision of %s class: %f" %(labels[i],precision[i]))
    print("Recall of %s class: %f" %(labels[i],recall[i]))
    print("F1-Score of %s class: %f" %(labels[i],f1Score[i]),"\n")


# In[6]:




# In[ ]:



