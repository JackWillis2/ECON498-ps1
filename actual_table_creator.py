from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import csv
pd.options.mode.chained_assignment = None

df=pd.read_csv("./parsed_files/weatherchanneldata.csv")
print(df)
actual_weather=df[df.time_backstep==1]
actual_weather["weather_precip_1period_diff"]=actual_weather.weather_precip.diff(periods=1)
actual_weather["weather_precip_2period_diff"]=actual_weather.weather_precip.diff(periods=2)
actual_weather["weather_humid_1period_diff"]=actual_weather.weather_humid.diff(periods=1)
actual_weather["weather_humid_2period_diff"]=actual_weather.weather_humid.diff(periods=2)
actual_weather["weather_temp_1period_diff"]=actual_weather.weather_temp.diff(periods=1)
actual_weather["weather_temp_2period_diff"]=actual_weather.weather_temp.diff(periods=2)

print(actual_weather)