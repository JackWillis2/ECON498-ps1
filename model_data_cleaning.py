import os
import glob
import pandas as pd
import csv
from sklearn.covariance import EmpiricalCovariance

pd.options.mode.chained_assignment = None

df=pd.read_csv("./parsed_files/weatherchanneldata.csv")

def create_dummies(x):
    ret = 0
    if (x == "Light Rain"):
        ret = 1
    elif (x == "Showers"):
        ret = 1
    elif (x == "Few Showers"):
    	ret = 1
    elif (x == "Rain"):
    	ret = 1
    elif (x == "Heavy Rain"):
    	ret = 1
    elif (x == "Scattered Thunderstorms"):
    	ret = 1
    elif (x == "Thunderstorms"):
    	ret = 1
    elif (x == "Isolated Thunderstorms"):
    	ret = 1

    return ret
def daytime_or_night(x):
	ret=0
	(hours,noon_marker)=x.split(":")
	hours=float(hours)
	if ("pm" in noon_marker):
		if (hours>7) & (hours !=12):
			ret=1
	else:
		if (hours<7) or (hours==12):
			ret=1
	return ret
df2=pd.DataFrame()
for i in range(1,16):
    actual_weather=df[df.time_backstep==i]
    print(actual_weather)
    actual_weather["weather_humid_1period_diff"]=actual_weather.weather_humid.diff(periods=1)
    actual_weather["weather_humid_2period_diff"]=actual_weather.weather_humid.diff(periods=2)
    actual_weather["weather_temp_1period_diff"]=actual_weather.weather_temp.diff(periods=1)
    actual_weather["weather_temp_2period_diff"]=actual_weather.weather_temp.diff(periods=2)
    actual_weather.fillna(value=0,inplace=True)
    actual_weather = actual_weather.iloc[2:]

    actual_weather['if_daytime']=actual_weather.weather_time.apply(daytime_or_night)
    actual_weather['if_raining']=actual_weather.weather_condition

    actual_weather['weather_feels']=actual_weather['weather_feels']-actual_weather['weather_temp']
    actual_weather=actual_weather.reset_index(drop=True)
    actual_weather.drop(['weather_time'], 1, inplace=True)
    actual_weather.drop(['weather_date'], 1, inplace=True)
    actual_weather.drop(['weather_condition'], 1, inplace=True)
    actual_weather.drop(['Unnamed: 0'], 1, inplace=True)
    df2 = df2.append(actual_weather, ignore_index=True)
print(df2)
df2.to_csv("parsed_files/actual_weather.csv")

