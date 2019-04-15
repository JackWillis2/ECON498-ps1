import os
import glob
import pandas as pd
import csv
import numpy as np
from sklearn.covariance import EmpiricalCovariance
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

df1=pd.read_csv("./parsed_files/actual_weather.csv")

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
    #plt.show()
    #plt.close()
correlation_matrix(df1)
#print(df1.groupby('if_raining').mean())

df1 = df1.sample(frac=1).reset_index(drop=True)
data = df1.iloc[:,2:11].values

target = df1.iloc[:,12]

data_training, data_test, target_training, target_test = train_test_split(data, target, test_size = 0.25, random_state = 0)

print(data.shape)
print(target.shape)
print(data_training.shape)
print(data_test.shape)
print(target_training.shape)
print(target_test.shape)


logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')


sample_leaf_options = [1,5,10,50,100,200,500]
limit=0
for leaf_size in sample_leaf_options :
    for x in range(100,1000,100):
        randforest = RandomForestClassifier(n_estimators=x, max_depth=3, random_state=0, min_samples_leaf=leaf_size)
        randforest.fit(data_training,target_training)
        score=randforest.score(data_test, target_test)
        if (score<limit) :
            break
        limit=score
        opt_leaf=leaf_size
        opt_trees=x

print(opt_leaf,opt_trees)
randforest = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0, min_samples_leaf=opt_leaf)
linearsupportvector = LinearSVC(random_state=0, tol=1e-5, multi_class='crammer_singer')

logreg.fit(data_training,target_training)
randforest.fit(data_training,target_training)
linearsupportvector.fit(data_training,target_training)
print(randforest.feature_importances_)
prediction_log = logreg.predict(data_test)
prediction_randforest=randforest.predict(data_test)
prediction_linearsupportvector=linearsupportvector.predict(data_test)
print(logreg.score(data_test, target_test))
print(randforest.score(data_test, target_test))
print(linearsupportvector.score(data_test, target_test))


kfold_machine = KFold(n_splits = 4)
kfold_machine.get_n_splits(data)
#for training_index, test_index in kfold_machine.split(data):
    #print("Training: ", training_index)
    #print("Test: ", test_index)
    #data_training, data_test = data[training_index], data[test_index]
    #target_training, target_test = target[training_index], target[test_index]
    #logreg.fit(data_training,target_training)
    #randforest.fit(data_training,target_training)
    #linearsupportvector.fit(data_training,target_training)
    #prediction_log = logreg.predict(data_test)
    #prediction_randforest=randforest.predict(data_test)
    #prediction_linearsupportvector=linearsupportvector.predict(data_test)
    #print(logreg.score(data_test, target_test))
    #print(randforest.score(data_test, target_test))
    #print(linearsupportvector.score(data_test, target_test))
