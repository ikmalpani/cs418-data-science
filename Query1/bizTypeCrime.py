'''
Created on Apr 17, 2018

@author: jaspreetsohal

query1: Report of types of crime (Assault, Battery, etc) within 3 blocks of (a) Grocery Stores (b) Schools, and (c) Restaurants.
Year, Business Type (a,b,c), Business Name, Address, Has Tobacco License, Has Liquor License, Crime Type, #Crimes, #Arrests, #On Premises
'''

import pandas as pd
# import numpy as np
import math
# import sys

#GLOBAL VARIABLES
radius = 0.029698

bizType = pd.read_csv('Q1Business.csv')

crimes = pd.read_csv('Crimes.csv',usecols=['Block','Primary Type','Arrest','Latitude','Longitude','Tract','Year']) 
crimes['Arrest'].replace([0,1],[0,1],inplace=True)                  #replace False with 0 and True with 1
crimes['uid'] = 0
# crimes = crimes.sample(n = 1000, random_state=2)

biz = bizType.groupby(['Latitude','Longitude']).agg({'Account Number':'first','License Id':'first','Legal Name':'first','Doing Business As Name':'first','Address':'first','License Code':'first',
                                                     'License Description':'first','Business Type':'first','FIPS':'first','Tract':'first','Block':'first'})
biz = biz.reset_index()
biz['#OnPremises'] = 0
#biz.to_csv('test.csv',sep=',')


def findCrimes():
    print('Please Wait.')
    for b_index, b in biz.iterrows():
        print('.', end ='', flush = True)
        noOnPremises = 0
        for c_index, crime in crimes.iterrows():
            crime_lat = round(crime['Latitude'], 8)
            crime_lng = round(crime['Longitude'], 8)
            biz_lat = round(b['Latitude'], 8)
            biz_lng = round(b['Longitude'], 8)
            
            latDiff = round(abs(crime_lat - biz_lat), 8)
            lngDiff = round(abs(abs(crime_lng) - abs(biz_lng)), 8)
            
            latDiffSquare = latDiff * latDiff
            lngDiffSquare = lngDiff * lngDiff
            
            dist = math.sqrt(latDiffSquare + lngDiffSquare)
            
            if dist < radius:
                crimes.loc[c_index,'uid'] = b['License Id']
                               
            if latDiff < 0.00001 and lngDiff < 0.00001:
                noOnPremises = noOnPremises + 1
                
        biz.loc[b_index,'#OnPremises'] = noOnPremises

tobacco = [1781, 1782]
liquor = [1470, 1481, 1477, 1471]

if __name__ == '__main__':
    findCrimes()
    crimes.to_csv('test2.csv',sep=',')
#    biz.to_csv('biz.csv',sep=',')

    crimesGrouped = crimes.groupby(['uid','Primary Type','Year']).agg({'Primary Type':'count','Arrest':'sum'})
    crimesGrouped = crimesGrouped.rename(columns={'Primary Type':'Crime Type','Primary Type':'#Crimes'})
    crimesGrouped = crimesGrouped.reset_index()
#    crimesGrouped.to_csv('test3.csv',sep=',')

    biz = biz.rename(columns={'License Id':'uid'})
    
    crimesBizType = biz.merge(crimesGrouped, on='uid')
#    crimesBizType.to_csv('test4.csv',sep=',')

    crimesBizType['Has Tobacco License'] = ''
    crimesBizType['Has Liquor License'] = ''
    
    for index, b in crimesBizType.iterrows():
        if b['License Code'] in tobacco:
            crimesBizType.loc[index,'Has Tobacco License'] = 'TRUE'
        else: 
            crimesBizType.loc[index,'Has Tobacco License'] = 'FALSE'
            
        if b['License Code'] in liquor:
            crimesBizType.loc[index,'Has Liquor License'] = 'TRUE'
        else: 
            crimesBizType.loc[index,'Has Liquor License'] = 'FALSE'
    
#    crimesBizType.to_csv('test4.csv',sep=',')

    result = crimesBizType[['Year','Business Type','Doing Business As Name','Address','Has Tobacco License','Has Liquor License','Primary Type','#Crimes','Arrest','#OnPremises']]
    result = result.rename(columns={'Doing Business As Name':'Business Name','Arrest':'#Arrests','Primary Type':'Crime Type'})

    result.to_csv('Query1_Results.csv',sep=',')
    
    print()
    print('Done.')
    
    
    
    
    
    
