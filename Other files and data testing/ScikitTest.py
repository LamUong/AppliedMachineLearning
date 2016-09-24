import numpy
import csv 
import re
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
import load
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
					else:
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
	a = LogisticRegression()
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

	
import csv


x,y,z = loaddata()
Y_All = load.load_y()

def K_fold_Cross_Validate(x,y,k=5):
	Testsetsize = len(x)/k
	splitBegin = 0
	splitEnd = Testsetsize
	while splitEnd <len(x):

		x_test = x[splitBegin:splitEnd]
		y_test = y[splitBegin:splitEnd]

		x_train = x[:splitBegin] +x[splitEnd:]
		y_train = y[:splitBegin] +y[splitEnd:]

		print learnandpredict(x_train,y_train,x_test,y_test)

		splitEnd +=  Testsetsize
		splitBegin +=  Testsetsize

K_fold_Cross_Validate(x,Y_All,k=5)


