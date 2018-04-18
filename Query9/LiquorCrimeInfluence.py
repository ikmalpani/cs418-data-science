'''
Created on Apr 14, 2018

@author: jaspreetsohal

Functionality: Does having a liquor license influence crime incidents in the neighborhood?
'''

import pandas as pd
import sys
import math

#GLOBAL VARIABLES
radius = 0.029698
# lngRad = 0.029698     #longitude radius
# latRad = 0.024157     #latitude radius

# bizfile = sys.argv[1]
crimefile = sys.argv[1]

bizfile = 'LiquorLicenses.csv'
# crimefile = 'Crimes_2001_to_present.csv'

liqLicBiz = pd.read_csv(bizfile, usecols=['Account Number','Latitude','Longitude','Block','Tract'])
# liqLicBiz = liqLicBiz.sample(n = 20, random_state=2)              #REMOVE THIS: SAMPLING DATA
liqLicBiz['#Crimes'] = 0
liqLicBiz['#Arrests'] = 0

crimes = pd.read_csv(crimefile, usecols=['ID','Arrest','Latitude','Longitude'])
crimes = crimes.sample(n = 5000, random_state=2)                    #taking random sample of size 5000 from the original file | random_state(for reproducibility) will reproduce same random rows each time
crimes['Arrest'].replace([0,1],[0,1],inplace=True)                  #replace False with 0 and True with 1

def crimesInNeighborhood():
    print('Please Wait')
    for biz_index, biz in liqLicBiz.iterrows():
#         print(biz_index)
        print('.', end='', flush = True)
        noCrimes = 0
        noArrests = 0
        for crime_index, crime in crimes.iterrows():
            crime_lat = round(crime['Latitude'], 8)
            crime_lng = round(crime['Longitude'], 8)
            biz_lat = round(biz['Latitude'], 8)
            biz_lng = round(biz['Longitude'], 8)
            
            latDiff = round(abs(crime_lat - biz_lat), 8)
            lngDiff = round(abs(abs(crime_lng) - abs(biz_lng)), 8)
            
            latDiffSquare = latDiff * latDiff
            lngDiffSquare = lngDiff * lngDiff
            
            dist = math.sqrt(latDiffSquare + lngDiffSquare)
            if dist < radius: 
                noCrimes = noCrimes + 1
                
                if crime['Arrest'] == 1:
                    noArrests = noArrests + 1 
                
                    
        liqLicBiz.loc[biz_index,'#Crimes'] = noCrimes
        liqLicBiz.loc[biz_index,'#Arrests'] = noArrests

if __name__ == '__main__':
    crimesInNeighborhood()
    
    liquorCrimes = liqLicBiz[['Tract','Block','Account Number','#Crimes', '#Arrests']]
#     liquorCrimes = liquorCrimes.groupby(['Tract','Block']).agg({'Account Number':'count','#Crimes':'sum','#Arrests':'sum'})
    liquorCrimes = liquorCrimes.groupby(['Tract','Block']).agg({'Account Number':'count','#Crimes':'first','#Arrests':'first'})
    liquorCrimes = liquorCrimes.rename(columns = {'Account Number':'#BusinessWithLiquorLicense'})
    liquorCrimes = liquorCrimes.reset_index()

    liquorCrimes.to_csv('Query9_Results.csv',sep=',')
    print()
    print('Done.')
    
    
    
    
    
    
    