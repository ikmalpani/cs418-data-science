import pandas as pd
import csv

yelp = pd.read_csv('/Users/yashikagoyal/PycharmProjects/yelp_rating_food_inspection/yelp_address_normalized.csv', usecols=['name', "address", 'rating_y'])

yelp['name'] = yelp['name'].str.upper()
yelp['address'] = yelp['address'].str.upper()




food_inspections = pd.read_csv('/Users/yashikagoyal/PycharmProjects/yelp_rating_food_inspection/food_address_normalized.csv', usecols=['AKA Name','DBA Name','Address','City','State','Zip','Inspection Date','Results','License #'])

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
        #print(temp[0]['DBA Name'])
        yes_count = yes_count + 1

        for t in temp.iterrows():
            #print(t[1])
            print("yyyyy")
            print(t)
            if  restaurant['address'] == (t[1].Address):
                print("yessss")
                l1 = list()
                l1.append(t[0])
                l1.append(t[1].Address)
                l1.append(t[1].License)
                l1.append(restaurant['rating_y'])
                yelp_name.append(l1)
                print(l1)


        #temp = temp['DBA Name']


        #print(temp)
        print("XXXxxxxx")
        #restaurant['name'].replace(temp)
        #print(restaurant)

    else:
        no_count = no_count + 1

print(yes_count)
print(no_count)

rest_name_file = open('yelp_inspection_name.csv' , 'w', newline='')
writer_rest = csv.writer(rest_name_file)

for row in yelp_name:
    writer_rest.writerow(row)







'''

import pandas as pd
import sys

yelp = pd.read_csv('restaurants_60601-60606.csv', usecols=['restaurantID', 'name', 'address'])
yelp.columns = ['SourceID', 'Name', 'Address']
yelp = yelp[yelp['Name'].str.startswith("M")]
yelp['Name'] = yelp['Name'].str.upper()
print(yelp.head())

food_inspections = pd.read_csv('Food_Inspections.csv', usecols=['Inspection ID', 'DBA Name', 'Risk'])
food_inspections.columns = ['SourceID', 'Name', 'Risk']
food_inspections = food_inspections[food_inspections['Name'].str.startswith("M")]
print(food_inspections.head())

# print(yelp.join(food_inspections, on='Name', how='outer', sort=False))

yelp_inspections = pd.DataFrame()
yelp_inspections.cols = ['SourceID', 'Address', 'Name', 'DBA Name', 'Risk']

yes_count = 0
no_count = 0

for index, restaurant in yelp.iterrows():
	if food_inspections['Name'].str.contains(restaurant['Name']).any():
		print(food_inspections['Name'], restaurant['Name'])
		yes_count += 1
	else:
		#print(restaurant['Name'])
		no_count += 1
print(yes_count)
print(no_count)

'''