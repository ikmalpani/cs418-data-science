import pandas as pd
import csv

yelp = pd.read_csv('yelp_address_normalized.csv', usecols=['name', "address", 'rating_y'])

yelp['name'] = yelp['name'].str.upper()
yelp['address'] = yelp['address'].str.upper()




food_inspections = pd.read_csv('food_address_normalized.csv', usecols=['AKA Name','DBA Name','Address','City','State','Zip','Inspection Date','Results','License #'])

food_inspections['AKA Name'] = food_inspections['AKA Name'].str.upper()
food_inspections['DBA Name'] = food_inspections['DBA Name'].str.upper()
food_inspections = food_inspections.rename(index=str, columns={"License #": "License"})


food_inspections = food_inspections.groupby('AKA Name').first()

yes_count = 0
no_count = 0

yelp_inspection_match = pd.DataFrame()
yelp_name = list()
l = list()
l.append('AKA Name')
l.append('Address')
l.append('License')
l.append('Rating')
yelp_name.append(l)

for index, restaurant in yelp.iterrows():
    if food_inspections['DBA Name'].str.contains(restaurant['name']).any() :
        temp = food_inspections[food_inspections['DBA Name'].str.contains(restaurant['name'])]
        
        yes_count = yes_count + 1

        for t in temp.iterrows():
            
            if  restaurant['address'] == (t[1].Address):
                
                l1 = list()
                l1.append(t[0])
                l1.append(t[1].Address)
                l1.append(t[1].License)
                l1.append(restaurant['rating_y'])
                yelp_name.append(l1)
                


        

    else:
        no_count = no_count + 1



rest_name_file = open('yelp_inspection_name.csv' , 'w', newline='')
writer_rest = csv.writer(rest_name_file)

for row in yelp_name:
    writer_rest.writerow(row)






