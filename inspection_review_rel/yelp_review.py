import csv
import sys
import pandas as pd

final = []
with open('reviews_60601-60606.csv') as csv_file:
    count = 0

    for line in csv.reader(csv_file):
        row = ','.join(line)
        rows = row.split(',')
        rows[3:-6] = [''.join(rows[3:-6])]
        count += 1
        print(rows)
        if len(rows) != 10:
            print(rows)
            #sys.exit(1)
        final.append(rows)


file = open('rev_60601-07.csv' , 'w', newline='')
writer_rest = csv.writer(file)

for row in final:
    writer_rest.writerow(row)
