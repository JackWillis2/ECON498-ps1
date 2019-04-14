import os
import glob
import pandas as pd
import csv
from sklearn.covariance import EmpiricalCovariance
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RandomForestClassifier
def correlation_matrix(df):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    plt.title('Correlation')
    labels=['feels','humid','temp','wind',  'humid_1diff','humid_2diff',    'temp_1diff',   'temp_2diff',   'if_raining',   'if_daytime']
    ax1.set_xticklabels(labels,fontsize=6)
    ax1.set_yticklabels(labels,fontsize=6)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
    plt.show()

correlation_matrix(df)
print(actual_weather.groupby('if_raining').mean())
#shows that data is super-correlated but good differentials between raining and not raining
