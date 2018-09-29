import csv
import pandas as pd

Ffile = pd.read_csv('business_viability.csv', usecols=['Alive for x years'])

print(Ffile.mean());






