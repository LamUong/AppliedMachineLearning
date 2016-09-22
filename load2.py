import numpy
import csv 
import re
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
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
					else  :
						data_row.append(float(row[i]))
				x.append(data_row)
		return x,y,z
		
	
def splitdata(data,splitratio):
	numpy.random.shuffle(data)
	mid = int(splitratio* len(data))
	train_x = data[:mid]
	test_x = data[mid:]
	return train_x,test_x

def learnandpredict(x,y):
	a = GaussianNB()
	Trained = a.fit(x, y)
	predict = Trained.predict(x)

	a=0
	b=0
	for i in range(0,len(y),1):
		if y[i] == predict[i]:
			a+=1
		else:
			b+=1
	return float(a)/(a+b)

x,y,z = loaddata()
print learnandpredict(x,y)

import csv
f = open("NaieveBayes.csv", "wt")
c = csv.writer(f)
for j in range(0,len(x[0]),1):
	x_new = []
	for i in range(0,len(x),1):
		x_new.append(x[i][j:j+1])
	value = learnandpredict(x_new,y)
	print "Hola"
	print z[j]
	print value
	if float(value)>0.5:
		f.write(",".join([str(value),str(z[j])]))
		f.write("\n")
f.close()
