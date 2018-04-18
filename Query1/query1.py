'''
Created on Apr 17, 2018

@author: jaspreetsohal

query1: Report of types of crime (Assault, Battery, etc) within 3 blocks of (a) Grocery Stores (b) Schools, and (c) Restaurants.
Year, Business Type (a,b,c), Business Name, Address, Has Tobacco License, Has Liquor License, Crime Type, #Crimes, #Arrests, #On Premises
'''

import pandas as pd
import numpy as np
import requests
import sys

filename = sys.argv[1]
# filename = 'Business_Licenses.csv'
biz = pd.read_csv(filename, usecols=['License Id','Account Number','Legal Name','Doing Business As Name','Address','License Code','License Description','Latitude','Longitude'])
biz['Business Type'] = '' 
biz = biz.sample(n = 5000, random_state=2)   #REMOVE THIS sampled data

restaurants = [1470,1472,1481,1477,1471,4405,1781,1782]
groceryStores = [1006,1474,1007,1016]
schools = [1584,1586,1585,1690,1023]

for index, b in biz.iterrows():
#     print(b['License Code'])
    if b['License Code'] in restaurants:
        biz.loc[index,'Business Type'] = 'restaurant'
    elif b['License Code'] in groceryStores:
        biz.loc[index, 'Business Type'] = 'grocery store'
    elif b['License Code'] in schools:
        biz.loc[index, 'Business Type'] = 'school'
    else:
        biz.loc[index, 'Business Type'] = np.nan
        
biz = biz.dropna(how='any')

def getFIPS():
    print('Please Wait')
    for index, b in biz.iterrows():
#         print(index)
        print('.', end ='', flush = True)
        parameters = {'latitude': b['Latitude'], 'longitude': b['Longitude'], 'format': 'json'}
        response = requests.get('https://www.broadbandmap.gov/broadbandmap/census/block', params=parameters)
        data = response.json()
        data = data['Results']['block'] 
        fips = data[0]['FIPS']
        biz.loc[index,'FIPS'] = fips
        tract = fips[5:11]
        biz.loc[index,'Tract'] = tract
        block = fips[-4:]
        biz.loc[index,'Block'] = block

if __name__ == '__main__':
    getFIPS()
    biz.to_csv('Q1Business.csv',sep=',')
    print()
    print('Done.')
    
    
    
    
    
    