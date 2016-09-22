import numpy
import csv 
import re
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

import sklearn
def loaddata():
	with open('full_data.csv', 'rb') as mycsvfile:
		thedata = csv.reader(mycsvfile)
		x = []
		y = []
		z = []
		count = 0

		for row in thedata:
			count += 1
			if count <2:
				for i in range(0,len(row),1):
					z.append(row[i]) 
			if count >=2:
				data_row = []
				for i in range(0,len(row),1):
					if i == 280:
						y.append(float(row[i]))
					elif i in [1,2,3,4]  or z[i] == '2014-09-28' or z[i] == '2013-09-22' or z[i] == '2013-02-17':
						data_row.append(float(row[i]))
				x.append(data_row)
		return x,y,z
		
	
def splitdata(data,splitratio):
	numpy.random.shuffle(data)
	mid = int(splitratio* len(data))
	train_x = data[:mid]
	test_x = data[mid:]
	return train_x,test_x

def learnandpredict(x_train,y_train,x_test,y_test):
	a = GaussianNB()
	Trained = a.fit(x_train, y_train)
	predict = Trained.predict(x_test)

	a=0
	b=0
	for i in range(0,len(y_test),1):
		if y_test[i] == predict[i]:
			a+=1
		else:
			b+=1
	return float(a)/(a+b)

x,y,z = loaddata()
x_train = x[:6000]
x_test = x[6000:]
y_train = y[:6000]
y_test = y[6000:]
print learnandpredict(x_train,y_train,x_test,y_test)

