Query 5:

Ensure that restaurants_60601-60606.csv is present in the directory.

On the command line/terminal run: python sentiment_analysis.py

Check sentiment_analysis.csv for the results required.

Query 6:

Ensure that sentiment_analysis.csv is present in the directory.

On the command line/terminal run: python sentiment_visualization.py

Check the plots that show the relationships between the ratings and sentiments.

Query 7:

Ensure that restaurants_60601-60606.csv, reviews_60601-60606.csv and the folders results and pickles are present in the directory.

Make sure that you have ran the script for Query 5 before running Query 7.

On the command line/terminal run: 

1. python yelp_review_prediction_clean.py -> Reading the csv and cleaning the data

2. python yelp_review_prediction_data.py -> Cleaning the data from Step 1. Make sure you have the pickels\X_train created. If not download it from: https://drive.google.com/file/d/1-mh0JxLTLxW1z66VviiV84QbRXdsLtr_/view?usp=sharing

3. python yelp_review_prediction_models.py -> ML models using a basic test train split

4. python yelp_review_prediction_models_cv.py -> ML models using Cross Validation

5. python yelp_review_prediction_models_nn.py -> LSTM using a basic test train split

6. python yelp_review_prediction_using_sentiment_analysis_split.py -> Same like step 3 but with data from sentiment analysis

7. python yelp_review_prediction_using_sentiment_analysis_cv.py -> Same like step 4 but with data from sentiment analysis

8. python yelp_review_prediction_models_nn_sentiments.py -> Same like step 5 but with data from sentiment analysis

If you run into any trouble(or it takes too long) while running the code, move to the folder notebooks and look at the iPython Notebooks with the results.
