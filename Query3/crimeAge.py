'''
Created on Apr 13, 2018

@author: jaspreetsohal

Functionality: Prevelant Crime statisitics and prevelant Age Group by Census Block
'''

import pandas as pd
import numpy as np
import sys

agefile = sys.argv[1]
# crimefile = sys.argv[2]

# agefile = 'AgeGroup2010.csv'
crimefile = 'Crimes.csv'

age = pd.read_csv(agefile, usecols=['FIPS','Tract','Block','0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80','total'])
age = age[np.isfinite(age['FIPS'])] 
age = age.loc[age['total'] != 0]

crimes = pd.read_csv(crimefile, usecols=['ID','Year','Primary Type','FIPS','Tract','Block'])
crimes = crimes[np.isfinite(crimes['FIPS'])]  

if __name__ == '__main__':
    print('Please Wait.')
#     groupedAgeCrime = crimes.merge(age, on='FIPS')

    ageGrouped = age.groupby(['Tract']).agg({'0to9':'sum','10to19':'sum','20to29':'sum','30to39':'sum','40to49':'sum','50to59':'sum','60to69':'sum','70to79':'sum','over80':'sum'})
    ageGrouped = ageGrouped.reset_index()
    prevalentAge = ageGrouped[['Tract','0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']]
    
    prevalentAge['AgeGroupPopulation'] = ageGrouped[['0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']].max(axis=1)
    prevalentAge['AgeGroup'] = ageGrouped[['0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']].idxmax(axis=1)
    prevalentAge = prevalentAge.reset_index()
    
    crimeGrouped = crimes.groupby(['Tract','Primary Type']).agg({'Primary Type':'count','Year':'first'})
    crimeGrouped = crimeGrouped.rename(columns = {'Primary Type': 'Crime Type', 'Primary Type': '#Crimes'})
    
    prevalentCrime = crimeGrouped.groupby(['Tract'])['#Crimes'].idxmax()
    prevalentCrime = crimeGrouped.loc[prevalentCrime]
    prevalentCrime = prevalentCrime.reset_index()
    
    prevalentAgeCrime = prevalentCrime.merge(prevalentAge, on='Tract')[['Tract','Primary Type','#Crimes','Year','AgeGroupPopulation','AgeGroup']]
    
    result = prevalentAgeCrime[['Year','Tract','AgeGroup','AgeGroupPopulation','Primary Type','#Crimes']]
    result = result.rename(columns = {'Tract':'Census Tract','Block':'Census Block','Primary Type':'Crime Type'})
    result.to_csv('Query3_Results.csv',sep=',')
    
#     GROUPING BY CENSUS TRACT + BLOCK
#         crimesGrouped = crimes.groupby(['FIPS','Tract','Block','Primary Type']).agg({'Primary Type':'count','Year':'first'})
#     crimesGrouped = crimesGrouped.rename(columns = {'Primary Type':'Crime Type','Primary Type':'#Crimes'})
#     crimesGrouped = crimesGrouped.reset_index()
#     crimesGrouped.to_csv('crimesTest.csv',sep=',')
#     
#     prevalentCrime = crimesGrouped.groupby(['Tract','Block','FIPS'])['#Crimes'].idxmax()
#     prevalentCrime = crimesGrouped.loc[prevalentCrime]
#     prevalentCrime.to_csv('pCrimes.csv',sep=',')
#     
#     ageGrouped = age.groupby(['FIPS','Tract','Block']).agg({'0to9':'sum','10to19':'sum','20to29':'sum','30to39':'sum','40to49':'sum','50to59':'sum','60to69':'sum','70to79':'sum','over80':'sum'})
#     ageGrouped = ageGrouped.reset_index()
#     prevalentAge = ageGrouped[['FIPS','Tract','Block','0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']]
#     
#     prevalentAge['AgeGroupPopulation'] = ageGrouped[['0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']].max(axis=1)
#     prevalentAge['AgeGroup'] = ageGrouped[['0to9','10to19','20to29','30to39','40to49','50to59','60to69','70to79','over80']].idxmax(axis=1)
#     prevalentAge = prevalentAge.reset_index()
#     prevalentAge.to_csv('pAge.csv',sep=',')
#     
#     prevalentAgeCrime = prevalentCrime.merge(prevalentAge, on='FIPS')[['Tract_x','Block_x','Primary Type','#Crimes','Year','AgeGroupPopulation','AgeGroup']]
#     prevalentAgeCrime = prevalentAgeCrime.rename(columns = {'Tract_x':'Tract','Block_x':'Block'})
#     
#     result = prevalentAgeCrime[['Year','Tract','Block','AgeGroup','AgeGroupPopulation','Primary Type','#Crimes']]
#     result = result.rename(columns = {'Tract':'Census Tract','Block':'Census Block','Primary Type':'Crime Type'})
#     result.to_csv('Crime_AgeGroup_Result.csv',sep=',')
    
    print('Done.')
     
    