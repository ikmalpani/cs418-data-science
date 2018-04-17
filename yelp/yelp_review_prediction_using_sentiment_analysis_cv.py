
# coding: utf-8

# In[13]:

import pandas as pd
import re
import nltk
import pickle
import xgboost as xgb
from sklearn import feature_extraction, model_selection
from sklearn import metrics, svm, tree, ensemble, linear_model, naive_bayes
from sklearn.model_selection import train_test_split
import warnings; warnings.simplefilter('ignore')
from imblearn.over_sampling import SMOTE


# In[2]:

yelp_analyzed = pd.read_csv('sentiment_analysis_output.csv')


# In[3]:

yelp_analyzed['sentiment'] = [1 if x=='positive' else 2 for x in yelp_analyzed['sentiment']]


# In[4]:

fileObject = open('pickels/clean_reviews','rb')  
cleaned_reviews = pickle.load(fileObject)


# In[5]:

yelp_analyzed['comment'] = cleaned_reviews


# In[6]:

X = yelp_analyzed[['comment', 'sentiment', 'polarity', 'subjectivity']]


# In[7]:

Y = yelp_analyzed[['rating']]


# In[8]:

def vectorization(train):
    vec = feature_extraction.text.TfidfVectorizer(min_df = 0.00125, max_df = 0.7, sublinear_tf=True, use_idf=True, stop_words=u'english', analyzer= 'word', ngram_range=(1,5),lowercase=True)
    train_vectors = vec.fit_transform(train)
    return train_vectors


# In[9]:

train_vectors = vectorization(X['comment'])


# In[10]:

train_X = pd.DataFrame(train_vectors.toarray())
train_X['sentiment'] = X['sentiment'].tolist()
train_X['polarity'] = X['polarity'].tolist()
train_X['subjectivity'] = X['subjectivity'].tolist()


# In[11]:

clfs = [naive_bayes.BernoulliNB(),svm.SVC(kernel='rbf', gamma=0.58, C=0.81),tree.DecisionTreeClassifier(random_state=0),ensemble.RandomForestClassifier(criterion='entropy', n_jobs = 10),linear_model.LogisticRegression(),linear_model.SGDClassifier(),ensemble.GradientBoostingClassifier(),xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)]


# In[ ]:

for clf in clfs:
    clf.fit(train_X, Y)
    preds = model_selection.cross_val_predict(clf, train_X, Y, cv=10)
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



