'''
Created on Apr 9, 2018

@author: jaspreetsohal

Functionality: Get Block corresponding to Latitude and Longitude
'''

import pandas as pd
import numpy as np
import requests
import sys

filename = sys.argv[1]
# filename = 'Crimes2010.csv'
crimes = pd.read_csv(filename, usecols=['ID','Primary Type','Community Area','Arrest','Year','Latitude','Longitude'])
crimes = crimes.sample(n = 5000, random_state=2)                    #taking random sample of size 5000 from the original file | random_state(for reproducibility) will reproduce same random rows each time
crimes = crimes[np.isfinite(crimes['Latitude'])]    
crimes['FIPS'] = 0 
crimes['Tract'] = 0
crimes['Block'] = 0

def getFIPS():
    print('Please Wait...')
    for index, crime in crimes.iterrows():
#         print(index)
        print('.', end='',flush=True)
        parameters = {'latitude': crime['Latitude'], 'longitude': crime['Longitude'], 'format': 'json'}
        response = requests.get('https://www.broadbandmap.gov/broadbandmap/census/block', params=parameters)
        data = response.json()
        data = data['Results']['block'] 
        fips = data[0]['FIPS']
        crimes.loc[index,'FIPS'] = fips
        tract = fips[5:11]
        crimes.loc[index,'Tract'] = tract
        block = fips[-4:]
        crimes.loc[index,'Block'] = block

if __name__ == '__main__':
    getFIPS()
    crimes.to_csv('Crimes.csv',sep=',')
    print()
    print('Done.')

