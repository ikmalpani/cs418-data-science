
# coding: utf-8

# In[1]:

import warnings
warnings.simplefilter('ignore')
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import log_loss
import pandas as pd
import datetime
import copy
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import csv


# In[2]:

c_data=pd.read_csv('Chicago_Master new.csv')    

c_data.Date = pd.to_datetime(c_data.Date, format = '%Y/%m/%d')

c_data.drop(['Max Temperature', 'Min Temperature'], inplace = True, axis = 1)

year = [i.strftime('%Y') for i in c_data['Date']]
c_data['Month']=[i.strftime('%m') for i in c_data['Date']]
c_data['year']=year

c_data['day_of_week'] = c_data['Date'].dt.dayofweek
c_data['Date'] = [i.date() for i in c_data['Date']]
days_dict = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri',
                    5:'Sat', 6:'Sun'}
c_data = c_data.replace({'day_of_week':days_dict})
c_data.index = pd.DatetimeIndex(c_data.Date,inplace=True,axis=1)
c_data['SEASON'] = pd.cut(
    (c_data.index.dayofyear + 11) % 366,
    [0, 91, 183, 275, 366],
    labels=['Winter', 'Spring', 'Summer', 'Fall']
)
c_data['Weekend Day'] = np.where(((c_data['day_of_week'] == 'Sat') | (c_data['day_of_week'] == 'Sun')),1,0)
c_data = c_data[(c_data['SEASON']=='Summer')]


# In[3]:

crime=pd.read_csv('Crimes_-_2001_to_present.csv')

crime = crime[(crime['Primary Type']=='ROBBERY')]
crime.Date = pd.to_datetime(crime.Date, format = '%m/%d/%Y %I:%M:%S %p')
crime.drop_duplicates(subset=['ID', 'Case Number'], inplace=True)
crime = crime.dropna()
crime.drop(['ID','Case Number','IUCR','FBI Code','Updated On','Location',
                 'X Coordinate','Y Coordinate','Location'], inplace = True, axis = 1)
crime['minute']=[i.strftime('%M') for i in crime['Date']]
crime['Hour'] = [i.strftime('%H') for i in crime['Date']]
crime['Date'] = [i.date() for i in crime['Date']]
crime.index = pd.DatetimeIndex(crime.Date,inplace=True,axis=1)
Hour=crime['Hour']
Hour = pd.to_numeric(Hour, errors='coerce')

enc9111= LabelEncoder()
crime['minute'] = enc9111.fit_transform(crime['minute'].astype(str))


# In[4]:

crimef=crime.merge(c_data, on="Date", how = 'inner', validate="m:m")
crimef.drop(['Hour','Arrest','Beat', 'Domestic', 'District', 'Ward'], inplace = True, axis = 1)
crimef.drop(['Date','Location Description','year'], inplace = True, axis = 1)


# In[5]:

zipcode=pd.read_csv('Community area and zip code equivalency - Community area and zip code equ.csv')
crimeff = crimef.merge(zipcode[['CHGOCA', 'ZCTA5']], how='inner', left_on='Community Area', right_on='CHGOCA')

crimeff.rename(columns={'ZCTA5': 'Zipcode'}, inplace=True)
crimeff.drop(['CHGOCA','minute'], inplace = True, axis = 1)


# In[6]:

census = pd.read_csv('CCASF12010CMAP.csv')
census.rename(columns={'GeogKey': 'Community Area'}, inplace=True)


# In[7]:

crimefinal = crimeff.merge(census[['Community Area','Not Hispanic or Latino, White alone', 'Not Hispanic or Latino, Black or African American alone','Hispanic or Latino','Vacant Housing Units']],on='Community Area', how='left')
crimefinal.rename(columns={'Not Hispanic or Latino, White alone': 'white'}, inplace=True)
crimefinal.rename(columns={'Not Hispanic or Latino, Black or African American alone': 'BlackAf'}, inplace=True)
crimefinal.rename(columns={'Hispanic or Latino': 'HL'}, inplace=True)
crimefinal.rename(columns={'Vacant Housing Units': 'vacanthouse'}, inplace=True)
def normalize(data): 
    data = (data - data.min()) / (data.max() - data.min())
    return data

crimefinal['Latitude'] = normalize(crimefinal.Latitude)
crimefinal['Longitude'] = normalize(crimefinal.Longitude)
crimefinal['white'] = normalize(crimefinal.white)
crimefinal['BlackAf'] = normalize(crimefinal.BlackAf)
crimefinal['HL'] = normalize(crimefinal.HL)
crimefinal['vacanthouse'] = normalize(crimefinal.vacanthouse)         
crimefinal = crimefinal[(crimefinal['SEASON']=='Summer')]
crimefinal.drop(['white','HL','Primary Type'],inplace=True,axis=1)


# In[8]:

testdata = copy.deepcopy(crimefinal)
y = crimefinal[['Description']]
crimefinal.pop('Description')
crimefinal.drop(['Community Area'],inplace=True,axis=1)


# In[9]:

import copy

features = copy.deepcopy(crimefinal)
features.drop(['Block','Heating Degree Days', ' Dew Point','Year',
   ' Average Humidity', ' Max Humidity', ' Minimum Humidity',
   ' Precipitation', ' Sea Level Pressure', ' Average Wind Speed',
   ' Maximum Wind Speed', ' Visibility', ' Events', 'SEASON',
   'Zipcode', 'day_of_week', 'Weekend Day'],inplace=True,axis=1)


# In[11]:

X_train, X_test, y_train, y_test = train_test_split(features, y, test_size = 0.15, random_state = 0)

ylabel=LabelEncoder()
ylabel.fit(y_train)
y_train= ylabel.transform(y_train)
y_test= ylabel.fit_transform(y_test)

X_train["Mean Temperature"].fillna(X_train["Mean Temperature"].mean(), inplace=True)
X_test["Mean Temperature"].fillna(X_test["Mean Temperature"].mean(), inplace=True)

rand_forest = RandomForestClassifier()
rand_forest.fit(X_train, y_train)
y_predrf = rand_forest.predict(X_test)

print ("Accuracy is ", accuracy_score(y_test,y_predrf)*100)

fileObject = open('models/cw_r_forest','wb')
pickle.dump(rand_forest, fileObject) 
fileObject.close()


# In[12]:

label_mapping = dict(zip(ylabel.classes_, ylabel.transform(ylabel.classes_)))

fileObject = open('models/cw_label_mapping','wb')
pickle.dump(label_mapping, fileObject) 
fileObject.close()


# In[13]:

fileObject = open('models/test','wb')
pickle.dump(X_test, fileObject) 
fileObject.close()


# In[ ]:



