import os
import glob
import pandas as pd
import csv
from sklearn.covariance import EmpiricalCovariance
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RandomForestClassifier
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
actual_weather["weather_humid_1period_diff"]=actual_weather.weather_humid.diff(periods=1)
actual_weather["weather_humid_2period_diff"]=actual_weather.weather_humid.diff(periods=2)
actual_weather["weather_temp_1period_diff"]=actual_weather.weather_temp.diff(periods=1)
actual_weather["weather_temp_2period_diff"]=actual_weather.weather_temp.diff(periods=2)
actual_weather.fillna(value=0,inplace=True)
actual_weather = actual_weather.iloc[2:]
actual_weather['if_raining']=actual_weather.weather_condition.apply(create_dummies)
actual_weather['if_daytime']=actual_weather.weather_time.apply(daytime_or_night)

actual_weather['weather_feels']=actual_weather['weather_feels']-actual_weather['weather_temp']

actual_weather.drop(['weather_precip'], 1, inplace=True)
actual_weather.drop(['weather_time'], 1, inplace=True)
actual_weather.drop(['weather_date'], 1, inplace=True)
actual_weather.drop(['weather_condition'], 1, inplace=True)
actual_weather.drop(['time_backstep'], 1, inplace=True)
actual_weather.drop(['Unnamed: 0'], 1, inplace=True)
actual_weather.to_csv("parsed_files/actual_weather")

def correlation_matrix(df):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    plt.title('Correlation')
    labels=['feels','humid','temp','wind',	'humid_1diff','humid_2diff',	'temp_1diff',	'temp_2diff',	'if_raining',	'if_daytime']
    ax1.set_xticklabels(labels,fontsize=6)
    ax1.set_yticklabels(labels,fontsize=6)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
    plt.show()

correlation_matrix(df)
print(actual_weather.groupby('if_raining').mean())
#shows that data is super-correlated but good differentials between raining and not raining
