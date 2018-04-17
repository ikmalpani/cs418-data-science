
# coding: utf-8

# In[1]:

import warnings; warnings.simplefilter('ignore')
import pickle
import sys, os, re, csv, codecs, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers


# In[2]:

list_classes = [1, 2, 3, 4, 5]

fileObject = open('pickels/clean_reviews','rb')  
cleaned_reviews = pickle.load(fileObject)

fileObject = open('pickels/ratings','rb')  
ratings = pickle.load(fileObject)


# In[4]:

yelp_analyzed = pd.read_csv('sentiment_analysis_output.csv')
yelp_analyzed['sentiment'] = [1 if x=='positive' else 2 for x in yelp_analyzed['sentiment']]
yelp_analyzed['comment'] = cleaned_reviews

X = yelp_analyzed[['comment', 'sentiment', 'polarity', 'subjectivity']]
Y = yelp_analyzed[['rating']]


# In[5]:

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[6]:

max_features = 20000
tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(list(X_train['comment']))
list_tokenized_train = tokenizer.texts_to_sequences(X_train['comment'])
list_tokenized_test = tokenizer.texts_to_sequences(X_test['comment'])


# In[7]:

maxlen = 100
X_t = pad_sequences(list_tokenized_train, maxlen=maxlen)
X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)


# In[8]:

X_t = np.hstack((X_t,X_train['sentiment'].reshape(X_train['sentiment'].shape[0],1)))
#X_t = np.hstack((X_t,X_train['polarity'].reshape(X_train['polarity'].shape[0],1)))
#X_t = np.hstack((X_t,X_train['subjectivity'].reshape(X_train['subjectivity'].shape[0],1)))

X_te = np.hstack((X_te, X_test['sentiment'].reshape(X_test['sentiment'].shape[0],1)))
#X_te = np.hstack((X_te, X_test['polarity'].reshape(X_test['polarity'].shape[0],1)))
#X_te = np.hstack((X_te, X_test['subjectivity'].reshape(X_test['subjectivity'].shape[0],1)))


# In[9]:

y_train = np.asarray(y_train)
y_test = np.asarray(y_test)


# In[10]:

inp = Input(shape=(maxlen+1, ))
embed_size = 128
x = Embedding(max_features, embed_size)(inp)
x = LSTM(200, return_sequences=True,name='lstm_layer')(x)
x = GlobalMaxPool1D()(x)
x = Dropout(0.1)(x)
x = Dense(120, activation="relu")(x)
x = Dropout(0.1)(x)
x = Dense(60, activation="relu")(x)
x = Dropout(0.1)(x)
x = Dense(6, activation="sigmoid")(x)
model = Model(inputs=inp, outputs=x)
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[11]:

print("start fitting...")
model.fit(X_t,y_train, epochs=10, batch_size=32, validation_split=0.1)


# In[12]:

# evaluate the model
scores = model.evaluate(X_te, y_test)
print("\n%s: %.4f%%" % (model.metrics_names[1], scores[1]*100))
y_pred = model.predict(X_te, batch_size=1024)
y_classes = y_pred.argmax(axis=-1)


# In[13]:

accScore = metrics.accuracy_score(y_test,y_classes)

lbl = [1,2,3,4,5]
precision = metrics.precision_score(y_test,y_classes,average=None,labels=lbl)
recall = metrics.recall_score(y_test,y_classes,average=None,labels=lbl)
f1Score = metrics.f1_score(y_test,y_classes,average=None,labels=lbl)

print("\nOverall Acurracy: ",accScore,"\n")

for i in range(len(lbl)):
    print("Precision of %s class: %f" %(lbl[i],precision[i]))
    print("Recall of %s class: %f" %(lbl[i],recall[i]))
    print("F1-Score of %s class: %f" %(lbl[i],f1Score[i]),"\n") 


# In[ ]:



