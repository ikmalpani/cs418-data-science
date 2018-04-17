import sys
import geocoder
import pandas as pd
import numpy as np
import pickle
import csv

def ltlongfinder(addr):
    addr=str(addr)
    g = geocoder.google(addr)
    result=g.latlng
    return result

args = sys.argv[1:]
final = []

def get_row(args, i):
    result = ltlongfinder(args[i])
    Year = 2018
    latitude = result[0]
    longitude = result[1]
    Hour = args[i+1]
    minute = args[i+2]
    day_of_week = args[i+3]

    if day_of_week == 'Sat' or day_of_week == 'Sun':
    	day_of_week = int(1)
    else:
    	day_of_week = int(0)
    row = [2018, latitude, longitude,minute, Hour,day_of_week]
    return row

def get_predictions(row, final):
    crime = pd.DataFrame(columns=('Year', 'Latitude', 'Longitude', 'minute','Hour', 'Weekend Day'))
    crime.loc[len(crime)] = row

    fileObject = open('models/label_mapping','rb')  
    label_mapping = pickle.load(fileObject)


    fileObject = open('models/knn','rb')  
    clf = pickle.load(fileObject)
    preds = clf.predict_proba(crime)

    sample = [args[0]]
    final_knn = []
    i = 0
    for each in sample:
        for j in range(len(preds[i])):
            adder = []
            adder.append(each)
            adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
            adder.append('K Nearest Neighbour')
            adder.append(preds[i][j])
            final_knn.append(adder)
        i += 1
     
    fileObject = open('models/random_forest','rb')  
    clf = pickle.load(fileObject)
    preds = clf.predict_proba(crime)

    final_rforest = []
    i = 0
    for each in sample:
        for j in range(len(preds[i])):
            adder = []
            adder.append(each)
            adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
            adder.append('Random Forest')
            adder.append(preds[i][j])
            final_rforest.append(adder)
        i += 1

    fileObject = open('models/decision_tree','rb')  
    clf = pickle.load(fileObject)
    preds = clf.predict_proba(crime)

    final_dtree = []
    i = 0
    for each in sample:
        for j in range(len(preds[i])):
            adder = []
            adder.append(each)
            adder.append(list(label_mapping.keys())[list(label_mapping.values()).index(j)])
            adder.append('Decision Tree')
            adder.append(preds[i][j])
            final_dtree.append(adder)
        i += 1
    final += final_knn
    final += final_dtree
    final += final_rforest

for k in range(int(len(args)/4)):
    row_new = get_row(args, k*4)
    print (row_new)
    get_predictions(row_new, final)

print(final)
with open("address_op_crime.csv", "w", newline = '') as f:
    writer = csv.writer(f)
    writer.writerows(final)