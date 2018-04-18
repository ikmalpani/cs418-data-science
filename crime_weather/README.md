Query 10:

1. Ensure that there are 'CCASF12010CMAP.csv', 'Chicago_Master new.csv', and 'Community area and zip code equivalency - Community area and zip code equ.csv'

2. Download the crimes dataset from: https://drive.google.com/file/d/11psZu0BDaX_7xZnDBb_DW7xsOhUOG_Qi/view?usp=sharing and save it in this directory. (You can also use the file in the crime_classification folder in the root directory)

3. On the command line/terminal run: python weather_crime_model.py

4. Ensure that the cw_r_forest and cw_label_mapping files has been created in the models folder.

5. On the command line/terminal run: python weather_crime_model_evaluation.py zipcode

6. Check the results in 'crime_weather.csv'

Here the arguments are:
first argument: Zipcode 

Ex:
> python weather_crime_model_evaluation.py 60601

If you run into any trouble(or it takes too long) while running the code, move to the folder notebooks and look at the iPython Notebooks with the results.