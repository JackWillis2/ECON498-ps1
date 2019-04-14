# ECON498-ps1
This is the problem set for the Econ4980 Class

To use this scrapper and model builder

1. weather_scrapper.py
  This script takes HTML shots hourly of the Weather in Clemson, SC for 5 days. These get saved in the "HTML_files" folder and are later used.
2. weather_parser.py
  This script takes the previously scraped HTML from the Weather Channel and parses it for relevant information
3. model_data_cleaning.py
  This script constructs a new table from previously constructed tables for the prediction of raining. It takes text information on weather condition, time differentials, and time of day in order to create a new table for prediction
4. rain_predictor.py
  This script tries three classifiers (Random Forest, Ridge Regression Classifiers, and LogisticRegression) and returns the best model for predicting if it is raining based on the clean data found after model_data_cleaning.py. MatPlotLib is used to see correlation, and has to be clicked through in order to run total output.
