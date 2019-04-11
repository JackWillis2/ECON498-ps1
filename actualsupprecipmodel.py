from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import csv
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

actual_weather=df[df.time_backstep==1]
actual_weather["weather_precip_1period_diff"]=actual_weather.weather_precip.diff(periods=1)
actual_weather["weather_precip_2period_diff"]=actual_weather.weather_precip.diff(periods=2)
actual_weather["weather_humid_1period_diff"]=actual_weather.weather_humid.diff(periods=1)
actual_weather["weather_humid_2period_diff"]=actual_weather.weather_humid.diff(periods=2)
actual_weather["weather_temp_1period_diff"]=actual_weather.weather_temp.diff(periods=1)
actual_weather["weather_temp_2period_diff"]=actual_weather.weather_temp.diff(periods=2)
actual_weather['if_raining']=actual_weather.weather_condition.apply(create_dummies)
actual_weather['if_daytime']=actual_weather.weather_time.apply(daytime_or_night)
print(actual_weather.weather_time,actual_weather.if_daytime)


