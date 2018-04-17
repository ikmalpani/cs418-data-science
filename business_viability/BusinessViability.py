import csv
import pandas as pd
import time


food_inspection = pd.read_csv('Food_Inspections.csv', usecols=['DBA Name','Address','City','State','Zip','Inspection Date','Results','License #'])


food_inspection['License #'] = food_inspection['License #'].astype(str)


business_licenses = pd.read_csv('Business_Licenses-2.csv', usecols=['LICENSE STATUS CHANGE DATE','LICENSE NUMBER'])
y=0

business_licenses['LICENSE NUMBER'] = business_licenses['LICENSE NUMBER'].astype(str)
business_file = open('business_viability.csv' , 'w', newline='')
writer_business = csv.writer(business_file)

food_inspection = food_inspection.rename(index=str, columns={"License #": "LICENSE NUMBER"})

food_business = pd.merge(food_inspection, business_licenses, on='LICENSE NUMBER', how='left')


out_of_business = food_business[food_business['LICENSE STATUS CHANGE DATE'].isnull()]

food_business = food_business[food_business['LICENSE STATUS CHANGE DATE'].notnull()].sort_values(by='LICENSE NUMBER' ,ascending=True)




food_business = food_business[(pd.to_datetime(food_business['Inspection Date']) < pd.to_datetime(food_business['LICENSE STATUS CHANGE DATE']))]


temp1 = food_business.groupby(['LICENSE NUMBER'])
temp = temp1.first()


temp['Alive for x years'] = (pd.to_datetime(temp['LICENSE STATUS CHANGE DATE']) - pd.to_datetime(temp['Inspection Date']))

business_viability = list()
l = list()
l.append('Restaurant Name')
l.append('Address')
l.append('Failed inspection on')
l.append('Alive for x years')
business_viability.append(l)

for index, rest in temp.iterrows():
    if (rest["Results"] == 'Fail'):
        date_difference = pd.to_datetime(rest['LICENSE STATUS CHANGE DATE']) - pd.to_datetime(rest['Inspection Date'])

        l1 = list()
        l1.append(rest['DBA Name'])
        l1.append(rest['Address'])
        l1.append(rest['Inspection Date'])
        l1.append(date_difference.days/365)
        business_viability.append(l1)
        y = y + 1

    else:
        t = food_business[(food_business['DBA Name'] == rest['DBA Name'])  & (food_business['Address'] == rest['Address'])]

        try:
            t = t[t['Results']== 'Fail']
            t = t.iloc[1]
            date_difference = pd.to_datetime(t['LICENSE STATUS CHANGE DATE']) - pd.to_datetime(t['Inspection Date'])
            l1 = list()
            l1.append(rest['DBA Name'])
            l1.append(rest['Address'])
            l1.append(rest['Inspection Date'])
            l1.append(date_difference.days / 365)
            business_viability.append(l1)
            y = y + 1

        except:
            continue


for row in business_viability:
    writer_business.writerow(row)

