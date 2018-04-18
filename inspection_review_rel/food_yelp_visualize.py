import pandas as pd
import csv
import matplotlib.pyplot as plt

food_inspections = pd.read_csv('/Users/yashikagoyal/PycharmProjects/yelp-business/food_address_normalized.csv', usecols=['AKA Name','DBA Name','Address','City','State','Zip','Inspection Date','Results','License #','Inspection Type'])
food_inspections['AKA Name'] = food_inspections['AKA Name'].str.upper()
food_inspections['DBA Name'] = food_inspections['DBA Name'].str.upper()
food_inspections = food_inspections.rename(index=str, columns={"License #": "License"})
food_inspections = food_inspections.rename(index=str, columns={"DBA Name": "Name"})


yelp_inspection_name = pd.read_csv('/Users/yashikagoyal/PycharmProjects/yelp-business/yelp_inspection_name.csv')

integrated = pd.merge(food_inspections, yelp_inspection_name, on='License', how='inner')
number = integrated.groupby(['License'])
number = number[['Name', 'License', 'Address_x', 'Results']]
#print(number)

Rest_with_Results = []
l1 = list()
#l1.append("Restaurant Name")
l1.append("License #")
#l1.append("Address")
l1.append("Rating Average Yelp")
l1.append("#Fail")
l1.append("#Pass")
l1.append("#PassW/Conditions")
Rest_with_Results.append(l1)


pass_count01 = 0
fail_count01 = 0
conditional_count01 = 0
pass_count12 = 0
fail_count12 = 0
conditional_count12 = 0
pass_count23 = 0
fail_count23 = 0
conditional_count23 = 0
pass_count34 = 0
fail_count34 = 0
conditional_count34 = 0
pass_count45 = 0
fail_count45 = 0
conditional_count45 = 0

for r in number:


    passnumber = 0
    failnumber = 0
    conditionalnumber = 0

    for res in r[1].iterrows():
        if res[1].Results == 'Fail':
            failnumber +=1
        if res[1].Results == 'Pass':
            passnumber +=1
        if res[1].Results == 'Pass w/ Conditions':
            conditionalnumber +=1



    temp1 = list()
    #temp1.append(res[1].Name)
    temp1.append(res[1].License)
    #temp1.append(res[1].Address_x)
    temp1.append(res[1].Rating)
    temp1.append(failnumber)
    temp1.append(passnumber)
    temp1.append(conditionalnumber)
    Rest_with_Results.append(temp1)

    max = passnumber
    r = 'Pass'
    if max < failnumber:
        max = failnumber
        r = 'Fail'
    if max < conditionalnumber:
        max = conditionalnumber
        r = 'Conditional'

    if 0 < res[1].Rating <= 1.0:
        if r == 'Pass':
            pass_count01 = pass_count01 + 1
        elif r == 'Fail':
            fail_count01 = fail_count01 + 1
        else:
            conditional_count01 = conditional_count01 + 1

    if 1.0 <= res[1].Rating < 2.0:
        if r == 'Pass':
            pass_count12 = pass_count12 + 1
        elif r == 'Fail':
            fail_count12 = fail_count12 + 1
        else:
            conditional_count12 = conditional_count12 + 1
    if 2.0 <= res[1].Rating < 3.0:
        if r == 'Pass':
            pass_count23 = pass_count23 + 1
        elif r == 'Fail':
            fail_count23 = fail_count23 + 1
        else:
            conditional_count23 = conditional_count23 + 1

    if 3.0 <= res[1].Rating < 4.0:
        if r == 'Pass':
            pass_count34 = pass_count34 + 1
        elif r == 'Fail':
            fail_count34 = fail_count34 + 1
        else:
            conditional_count34 = conditional_count34 + 1

    if 4.0 <= res[1].Rating <= 5.0:
        if r == 'Pass':
            pass_count45 = pass_count45 + 1
        elif r == 'Fail':
            fail_count45 = fail_count45 + 1
        else:
            conditional_count45 = conditional_count45 + 1



rating = [(pass_count01, fail_count01,conditional_count01),
          (pass_count12, fail_count12, conditional_count12),
          (pass_count23, fail_count23, conditional_count23),
          (pass_count34, fail_count34, conditional_count34),
          (pass_count45, fail_count45, conditional_count45)]


df = pd.DataFrame.from_records(rating, index=['0-1','1-2','2-3', '3-4', '4-5'] ,columns=['Pass','Fail', 'Conditional'])


ax = df.plot.bar()
ax.set_ylabel('Restaurant Count')
ax.set_xlabel('Ratings')
plt.show()

food_file = open('numberOfResults.csv' , 'w', newline='')
writer_food = csv.writer(food_file)

for row in Rest_with_Results:
    writer_food.writerow(row)


