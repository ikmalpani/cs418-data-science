
# coding: utf-8

# In[194]:

import pandas as pd
import pandas as pd
import numpy as np
import requests
import pickle
import csv
import sys


# In[69]:

zcode = sys.argv[1]

# In[70]:

crime = pd.read_csv('Crimes_-_2001_to_present.csv')
zipcode = pd.read_csv('Community area and zip code equivalency - Community area and zip code equ.csv')


# In[71]:

crimeff = crime.merge(zipcode[['CHGOCA', 'ZCTA5']], how='inner', left_on='Community Area', right_on='CHGOCA')

crimeff = crimeff[(crimeff['ZCTA5']==zcode)]


# In[176]:

lat_long = crimeff[['Latitude','Longitude']].dropna().drop_duplicates()


# In[73]:

blocks = pd.DataFrame(columns = ['Block', 'FIPS', 'Tract'])   
blocks['Block'] = 0
blocks['FIPS'] = 0
blocks['Tract'] = 0

for index, crime in lat_long.iterrows():
    parameters = {'latitude': crime[0], 'longitude': crime[1], 'format': 'json'}
    response = requests.get('https://www.broadbandmap.gov/broadbandmap/census/block', params=parameters)
    data = response.json()
    data = data['Results']['block'] 
    fips = data[0]['FIPS']
    blocks.loc[index,'FIPS'] = fips
    tract = fips[5:11]
    blocks.loc[index,'Tract'] = tract
    block = fips[-4:]
    blocks.loc[index,'Block'] = block


# In[177]:

weather_dict = {'Month': [6,7,8,9], 'Mean Temperature': [73.021581, 75.003995, 73.409822, 68.271818]}
weather = pd.DataFrame(data=weather_dict)


# In[178]:

lat_long['Block'] = blocks['Block']


# In[179]:

lat_long['key'] = 1
weather['key'] = 1

lat_long = lat_long.merge(weather, on='key')
del lat_long['key']


# In[180]:

census = pd.read_csv('CCASF12010CMAP.csv')
census.rename(columns={'GeogKey': 'Community Area'}, inplace=True)
census.rename(columns={'Not Hispanic or Latino, Black or African American alone': 'BlackAf'}, inplace=True)
census.rename(columns={'Vacant Housing Units': 'vacanthouse'}, inplace=True)
census = census[['Community Area','BlackAf','vacanthouse']]


# In[181]:

c_area = pd.read_csv('Community area and zip code equivalency - Community area and zip code equ.csv')

c_area = c_area[(c_area['ZCTA5'] == zcode)]


# In[182]:

vacant_black = census.merge(c_area, left_on="Community Area", right_on="CHGOCA")[['BlackAf', 'vacanthouse']]


# In[183]:

lat_long['key'] = 1
vacant_black['key'] = 1

lat_long = lat_long.merge(vacant_black, on='key')
del lat_long['key']


# In[184]:

census_block = lat_long.pop('Block')


# In[185]:

fileObject = open('models/cw_r_forest','rb') 
clf = pickle.load(fileObject)
fileObject.close()
preds = clf.predict_proba(lat_long)


# In[187]:

fileObject = open('models/cw_label_mapping','rb')  
label_mapping = pickle.load(fileObject)
fileObject.close()


# In[191]:

final = []
i = 0
for each in census_block:
    for j in range(len(preds[i])):
        adder = []
        adder.append(each)
        adder.append(lat_long['Month'][i])
        adder.append(lat_long['Mean Temperature'][i])
        adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
        adder.append(preds[i][j])
        final.append(adder)
    i += 1


# In[195]:

with open("crime_weather.csv", "w", newline = '') as f:
    writer = csv.writer(f)
    writer.writerows(final)


# In[ ]:



