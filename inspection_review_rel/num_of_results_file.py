import pandas as pd

results = pd.read_csv('numberOfResults.csv')
food = pd.read_csv('/Users/yashikagoyal/Desktop/data analysis/Food_Inspections_60601_07.csv', usecols=['DBA Name', 'Address', 'License #'])
food = pd.merge(food, results, on='License #', how='inner' )
food = food.groupby("License #").first()

food.to_csv('food_results_rating.csv')
print(food)

