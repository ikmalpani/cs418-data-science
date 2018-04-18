import csv
import  pandas as pd

final = pd.read_csv('rev_60601-07.csv')
temp = final.groupby(["restaurantID"] ,axis=0)[['rating']].mean()
rating = pd.DataFrame(temp)
rating.to_csv('restID_rating.csv')
r = pd.read_csv('restID_rating.csv')
yelp_rest = pd.read_csv('restaurants_60601-60606.csv')

yelp_avg = pd.merge(yelp_rest, r, on= 'restaurantID', how='inner')

yelp_avg.to_csv('rev_60601-60606.csv')



