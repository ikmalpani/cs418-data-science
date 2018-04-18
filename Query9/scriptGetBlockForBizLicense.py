'''
Created on Apr 14, 2018

@author: jaspreetsohal

Functionality: Filter Business Licenses to Liquor Liceneses and get census block for businesses with liquor licenses
'''

import pandas as pd
import numpy as np
import requests
import sys

filename = sys.argv[1]

# filename = 'Business_Licenses.csv'
bizLic = pd.read_csv(filename, usecols=['License Id','Account Number','Legal Name','Address','License Code','License Description','Latitude','Longitude'])
array = [1470, 1471, 1475, 1477, 1481]                          # Tavern, Late Hour, Consumption On Premises-Incidental Activity, Outdoor Patio, Caterer's Liquor License
liquorLic = bizLic.loc[bizLic['License Code'].isin(array)]

liquorLic = liquorLic[np.isfinite(liquorLic['Latitude'])] 

bizLiquorLic = liquorLic.groupby(['Account Number']).agg({'Latitude':'first','Longitude':'first','Legal Name':'first','Address':'first'})
bizLiquorLic = bizLiquorLic.reset_index()   
   
bizLiquorLic['FIPS'] = 0 
bizLiquorLic['Tract'] = 0
bizLiquorLic['Block'] = 0

def getFIPS():
    print('Please Wait')
    for index, biz in bizLiquorLic.iterrows():
#         print(index)
        print('.', end ='', flush = True)
        parameters = {'latitude': biz['Latitude'], 'longitude': biz['Longitude'], 'format': 'json'}
        response = requests.get('https://www.broadbandmap.gov/broadbandmap/census/block', params=parameters)
        data = response.json()
        data = data['Results']['block'] 
        fips = data[0]['FIPS']
        bizLiquorLic.loc[index,'FIPS'] = fips
        tract = fips[5:11]
        bizLiquorLic.loc[index,'Tract'] = tract
        block = fips[-4:]
        bizLiquorLic.loc[index,'Block'] = block
        

if __name__ == '__main__':
    getFIPS()
    bizLiquorLic.to_csv('LiquorLicenses.csv',sep=',')
    print()
    print('Done.')
