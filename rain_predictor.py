import os
import glob
import pandas as pd
import csv
import numpy as np
from sklearn.manifold import Isomap
from sklearn.covariance import EmpiricalCovariance
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn import metrics
import matplotlib.gridspec as gridspec
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from matplotlib import pyplot as plt

df1=pd.read_csv("./parsed_files/actual_weather.csv")
df1=df1.sample(frac=1).reset_index(drop=True)

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

def svc_param_selection(X, y, nfolds):
	Cs = [0.001, 0.01, 0.1, 1, 10]
	gammas = [0.001, 0.01, 0.1, 1]
	param_grid = {'C': Cs, 'gamma' : gammas}
	grid_search = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=nfolds)
	grid_search.fit(X, y)
	grid_search.best_params_
	return grid_search.best_params_


def randforest_param_selection(X, y, nfolds):
	param_grid = {
	'bootstrap': [True],
	'max_depth': [80, 90, 100, 110],
	'max_features': [2, 3],
	'min_samples_leaf': [3, 4, 5],
	'min_samples_split': [8, 10, 12],
	'n_estimators': [100, 200, 300, 1000]
	}
	rf=RandomForestClassifier()
	grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
						  cv = 3, n_jobs = -1, verbose = 2)
	grid_search.fit(X, y)
	grid_search.best_params_
	return grid_search.best_params_


correlation_matrix(df1)
#print(df1.groupby('if_raining').mean())
data = df1.iloc[:,2:14].values

embedding = Isomap(n_components=3)
X_transformed = embedding.fit_transform(data)

target = df1.iloc[:,15]
catenc = pd.factorize(target)
target = catenc[0]

print(target)
data_training, data_test, target_training, target_test = train_test_split(data, target, test_size = 0.25, random_state = 25)

print(data.shape)
print(target.shape)
print(data_training.shape)
print(data_test.shape)
print(target_training.shape)
print(target_test.shape)

logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')


#randfor_best=randforest_param_selection(data_training,target_training,1)
#print(randfor_best)
#this is tuned
randforest = RandomForestClassifier(bootstrap=True, max_depth= 80, max_features=3, min_samples_leaf=3, min_samples_split=8, n_estimators=300)

#this is also tuned
linearsupportvector=SVC(C=10,gamma=0.001)

logreg.fit(data_training,target_training)
randforest.fit(data_training,target_training)
linearsupportvector.fit(data_training,target_training)

print(randforest.feature_importances_)

prediction_log = logreg.predict(data_test)
prediction_randforest=randforest.predict(data_test)
prediction_linearsupportvector=linearsupportvector.predict(data_test)

print("LogisticRegression:",logreg.score(data_test, target_test),)
print("Random Forest:",randforest.score(data_test, target_test))
print("SVM:",linearsupportvector.score(data_test, target_test))



kfold_machine = KFold(n_splits = 4)
kfold_machine.get_n_splits(data)
for training_index, test_index in kfold_machine.split(data):
	#print("Training: ", training_index)
	#print("Test: ", test_index)
	data_training, data_test = data[training_index], data[test_index]
	target_training, target_test = target[training_index], target[test_index]
	logreg.fit(data_training,target_training)
	randforest.fit(data_training,target_training)
	linearsupportvector.fit(data_training,target_training)
	prediction_log = logreg.predict(data_test)
	prediction_randforest=randforest.predict(data_test)
	prediction_linearsupportvector=linearsupportvector.predict(data_test)
	print("LogisticRegression:",logreg.score(data_test, target_test),)
	print("Random Forest:",randforest.score(data_test, target_test))
	print("SVM:",linearsupportvector.score(data_test, target_test))
