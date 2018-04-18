import  csv
yelp_normalized = []

yelp_n = open('yelp_address_normalized.csv' , 'w', newline='')
writer_yelp = csv.writer(yelp_n)


with open('rev_60601-60606.csv') as csv_file:
    for line in csv.reader(csv_file):
        address = line[7].split("(")[0]
        address = address.split("Chicago")[0]
        address = address.split("Ave")[0]
        address = address.split("Dr")[0]
        address = address.split("Pl")[0]
        address = address.split("Blvd")[0]
        address = address.split("St")[0]

        #name = line[2].split("Inc")[0]
        temp = list()
        temp.append(line[2])
        temp.append(address)
        temp.append(line[31])
        yelp_normalized.append(temp)
        #print(address)



for row in yelp_normalized:
    writer_yelp.writerow(row)

food_n = open('food_address_normalized.csv' , 'w', newline='')
writer_food = csv.writer(food_n)

food_normalized = []
with open('Food_Inspections_60601_07.csv') as food_file:
    for line1 in csv.reader(food_file):
        add = line1[6].split("AVE")[0]
        add = add.split("DR")[0]
        add = add.split("PL")[0]
        add = add.split("BLVD")[0]
        add = add.split("ST")[0]

        nam = line1[1].split("INC")[0]
        nam = line1[1].split("LLC")[0]
        nam = line1[1].split("LIC")[0]
        #address = address.split("St")[0]
        temp1 = list()
        temp1.append(line1[0])
        temp1.append(nam)
        temp1.append(line1[2])
        temp1.append(line1[3])
        #temp1.append(line1[6])
        temp1.append(add)
        temp1.append(line1[7])
        temp1.append(line1[8])
        temp1.append(line1[9])
        temp1.append(line1[10])
        temp1.append(line1[11])
        temp1.append(line1[12])
        food_normalized.append(temp1)
        print(temp1)

for row1 in food_normalized:
    writer_food.writerow(row1)
