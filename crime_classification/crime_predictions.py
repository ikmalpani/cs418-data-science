
# coding: utf-8

# In[1]:

import warnings
warnings.simplefilter('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import log_loss
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn import ensemble, metrics, tree


# In[2]:

crime=pd.read_csv('Crimes_-_2001_to_present.csv')


# In[3]:

crime.Date = pd.to_datetime(crime.Date, format = '%m/%d/%Y %I:%M:%S %p')
crime.drop_duplicates(subset=['ID', 'Case Number'], inplace=True)
crime = crime.dropna()
crime.drop(['ID','Case Number','IUCR','FBI Code','Updated On','Location',
                 'X Coordinate','Y Coordinate','Location'], inplace = True, axis = 1)
crime['minute']=[i.strftime('%M') for i in crime['Date']]
crime['Hour'] = [i.strftime('%H') for i in crime['Date']]
crime['Date'] = pd.to_datetime(crime['Date'], errors='coerce')
crime.index = pd.DatetimeIndex(crime.Date,inplace=True,axis=1)
Hour=crime['Hour']
Hour = pd.to_numeric(Hour, errors='coerce')
crime['SEASON'] = pd.cut(
    (crime.index.dayofyear + 11) % 366,
    [0, 91, 183, 275, 366],
    labels=['Winter', 'Spring', 'Summer', 'Fall']
)
ranges = [0,6,12,18,24]
l = ['Early Morning','Morning','Afternoon','Evening']
session=pd.cut(crime.Date.dt.hour,[-1,6,12,18,24],labels=['Early Morning','Morning','Afternoon','Evening']).astype('category')
crime['session']=session


# In[4]:

crime['Date'] = pd.to_datetime(crime['Date'], errors='coerce')
crime['day_of_week'] = crime['Date'].dt.dayofweek

days_dict = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri',
                    5:'Sat', 6:'Sun'}
crime = crime.replace({'day_of_week':days_dict})
crime.index = pd.DatetimeIndex(crime.Date,inplace=True,axis=1)
crime['Weekend Day'] = np.where(((crime['day_of_week'] == 'Sat') | (crime['day_of_week'] == 'Sun')),1,0)


# In[5]:

zipcode=pd.read_csv('Community area and zip code equivalency - Community area and zip code equ.csv')


# In[6]:

crimeff = crime.merge(zipcode[['CHGOCA', 'ZCTA5']], how='inner', left_on='Community Area', right_on='CHGOCA')
crimeff.rename(columns={'ZCTA5': 'Zipcode'}, inplace=True)
crimeff.drop(['CHGOCA'], inplace = True, axis = 1)
crimeff = crimeff[(crimeff['Zipcode'] > 60600) & (crimeff['Zipcode'] < 60608)]


# In[7]:

def normalize(data): 
    data = (data - data.min()) / (data.max() - data.min())
    return data

crimeff['Latitude'] = normalize(crimeff.Latitude)
crimeff['Longitude'] = normalize(crimeff.Longitude)


# In[8]:

crimeff.drop(['Date','Description','Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area','Zipcode'],inplace=True,axis=1)


# In[9]:

y=crimeff[crimeff.columns[1]]


# In[10]:

crimeff.pop('Primary Type')


# In[11]:

crimeff.drop(['Location Description'], inplace=True,axis=1)

import copy

features=copy.deepcopy(crimeff)


# In[12]:

X_train, X_test, y_train, y_test = train_test_split(features, y, test_size = 0.001, random_state = 0)


# In[13]:

X_train.drop(['Block'], inplace=True,axis=1)
test_addresses = X_test['Block']
X_test.drop(['Block'], inplace=True,axis=1)


# In[14]:

ylabel=LabelEncoder()
ylabel.fit(y_train)
y_train= ylabel.fit_transform(y_train)
y_test= ylabel.transform(y_test)

# enc91= LabelEncoder()
# X_train['Block'] = enc91.fit_transform(X_train['Block'].astype(str))
# X_test['Block'] = enc91.transform(X_test['Block'].astype(str))

enc931= LabelEncoder()
X_train['SEASON'] = enc931.fit_transform(X_train['SEASON'].astype(str))
X_test['SEASON'] = enc931.transform(X_test['SEASON'].astype(str))

#enc922= LabelEncoder()
#X_train['Location Description'] = enc922.fit_transform(X_train['Location Description'].astype(str))
#X_test['Location Description'] = enc922.transform(X_test['Location Description'].astype(str))

enc933= LabelEncoder()
X_train['session'] = enc933.fit_transform(X_train['session'].astype(str))
X_test['session'] = enc933.transform(X_test['session'].astype(str))

enc934= LabelEncoder()
X_train['day_of_week'] = enc934.fit_transform(X_train['day_of_week'].astype(str))
X_test['day_of_week'] = enc934.transform(X_test['day_of_week'].astype(str))


# In[15]:

label_mapping = dict(zip(ylabel.classes_, ylabel.transform(ylabel.classes_)))


# In[16]:

clf = KNeighborsClassifier()
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
accScore = metrics.accuracy_score(y_test,preds)
labels = range(32)

precision = metrics.precision_score(y_test,preds,average=None,labels=labels)
recall = metrics.recall_score(y_test,preds,average=None,labels=labels)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=labels)

print(clf)
print("\nOverall Acurracy: ",accScore,"\n")

preds = clf.predict_proba(X_test)

sample = test_addresses
final_knn = []
i = 0
for each in sample:
    for j in range(len(preds[i])):
        adder = []
        adder.append(each)
        adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
        adder.append('K Nearest Neighbour')
        adder.append(preds[i][j])
        final_knn.append(adder)
    i += 1


# In[17]:

clf = ensemble.RandomForestClassifier()
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
accScore = metrics.accuracy_score(y_test,preds)
labels = range(32)

precision = metrics.precision_score(y_test,preds,average=None,labels=labels)
recall = metrics.recall_score(y_test,preds,average=None,labels=labels)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=labels)

print(clf)
print("\nOverall Acurracy: ",accScore,"\n")

preds = clf.predict_proba(X_test)

sample = test_addresses

final_rforest = []
i = 0
for each in sample:
    for j in range(len(preds[i])):
        adder = []
        adder.append(each)
        adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
        adder.append('Random Forest')
        adder.append(preds[i][j])
        final_rforest.append(adder)
    i += 1


# In[18]:

clf = tree.DecisionTreeClassifier()
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
accScore = metrics.accuracy_score(y_test,preds)
labels = range(32)

precision = metrics.precision_score(y_test,preds,average=None,labels=labels)
recall = metrics.recall_score(y_test,preds,average=None,labels=labels)
f1Score = metrics.f1_score(y_test,preds,average=None,labels=labels)

print(clf)
print("\nOverall Acurracy: ",accScore,"\n")

preds = clf.predict_proba(X_test)

sample = test_addresses

final_dtree = []
i = 0
for each in sample:
    for j in range(len(preds[i])):
        adder = []
        adder.append(each)
        adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
        adder.append('Decision Tree')
        adder.append(preds[i][j])
        final_dtree.append(adder)
    i += 1


# In[19]:

with open("test_op_crime.csv", "w", newline = '') as f:
    writer = csv.writer(f)
    writer.writerows(final_dtree)
    writer.writerows(final_rforest)
    writer.writerows(final_knn)


# In[ ]:



