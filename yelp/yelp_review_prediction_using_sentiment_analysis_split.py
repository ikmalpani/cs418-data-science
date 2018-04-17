
# coding: utf-8

# In[47]:

import pandas as pd
import re
import nltk
import pickle
import xgboost as xgb
from sklearn import feature_extraction
from sklearn import metrics, svm, tree, ensemble, linear_model, naive_bayes
from sklearn.model_selection import train_test_split
import warnings; warnings.simplefilter('ignore')
from imblearn.over_sampling import SMOTE


# In[48]:

yelp_analyzed = pd.read_csv('sentiment_analysis_output.csv')


# In[49]:

yelp_analyzed['sentiment'] = [1 if x=='positive' else 2 for x in yelp_analyzed['sentiment']]


# In[50]:

fileObject = open('pickels/clean_reviews','rb')  
cleaned_reviews = pickle.load(fileObject)


# In[51]:

yelp_analyzed['comment'] = cleaned_reviews


# In[52]:

X = yelp_analyzed[['comment', 'sentiment', 'polarity', 'subjectivity']]


# In[53]:

Y = yelp_analyzed[['rating']]


# In[54]:

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[55]:

def vectorization(train,test):
    vec = feature_extraction.text.TfidfVectorizer(min_df = 0.00125, max_df = 0.7, sublinear_tf=True, use_idf=True, stop_words=u'english', analyzer= 'word', ngram_range=(1,5),lowercase=True)
    train_vectors = vec.fit_transform(train)
    test_vectors = vec.transform(test)
    return train_vectors,test_vectors


# In[56]:

train_vectors, test_vectors = vectorization(X_train['comment'], X_test['comment'])


# In[57]:

train_X = pd.DataFrame(train_vectors.toarray())
test_X = pd.DataFrame(test_vectors.toarray())


# In[58]:

train_X['sentiment'] = X_train['sentiment'].tolist()
train_X['polarity'] = X_train['polarity'].tolist()
train_X['subjectivity'] = X_train['subjectivity'].tolist()


# In[59]:

test_X['sentiment'] = X_test['sentiment'].tolist()
test_X['polarity'] = X_test['polarity'].tolist()
test_X['subjectivity'] = X_test['subjectivity'].tolist()


# In[60]:

sm = SMOTE(random_state=43)
train_X, y_train = sm.fit_sample(train_X, y_train)


# In[27]:

clfs = [naive_bayes.BernoulliNB(),svm.SVC(kernel='rbf', gamma=0.58, C=0.81),tree.DecisionTreeClassifier(random_state=0),ensemble.RandomForestClassifier(criterion='entropy', n_jobs = 10),linear_model.LogisticRegression(),linear_model.SGDClassifier(),ensemble.GradientBoostingClassifier(),xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)]


# In[28]:

for clf in clfs:
    clf.fit(train_X, y_train)
    preds = clf.predict(test_X)
    accScore = metrics.accuracy_score(y_test,preds)

    lbl = [1,2,3,4,5]
    precision = metrics.precision_score(y_test,preds,average=None,labels=lbl)
    recall = metrics.recall_score(y_test,preds,average=None,labels=lbl)
    f1Score = metrics.f1_score(y_test,preds,average=None,labels=lbl)

    print(clf)
    print("\nOverall Acurracy: ",accScore,"\n")

    for i in range(len(lbl)):
        print("Precision of %s class: %f" %(lbl[i],precision[i]))
        print("Recall of %s class: %f" %(lbl[i],recall[i]))
        print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[67]:

train_X = train_X.as_matrix()
test_X = test_X.as_matrix()


# In[63]:

clf = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
clf.fit(train_X, y_train)
preds = clf.predict(test_X)
accScore = metrics.accuracy_score(y_test,preds)

lbl = [1,2,3,4,5]
precision = metrics.precision_score(y_test,preds,average=None,labels=lbl)
recall = metrics.recall_score(y_test,preds,average=None,labels=lbl)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=lbl)

print(clf)
print("\nOverall Acurracy: ",accScore,"\n")

for i in range(len(lbl)):
    print("Precision of %s class: %f" %(lbl[i],precision[i]))
    print("Recall of %s class: %f" %(lbl[i],recall[i]))
    print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[68]:




# In[ ]:



