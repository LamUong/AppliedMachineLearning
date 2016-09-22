import load
import numpy
import math
import csv
from sklearn.naive_bayes import GaussianNB
def loaddata():
	with open('full_data.csv', 'rb') as mycsvfile:
		thedata = csv.reader(mycsvfile)
		x = []
		y = []
		count = 0
		for row in thedata:
			count += 1
			if count >=2:
				data_row = []
				for i in range(0,len(row),1):
					if i == 0:
						y.append(float(row[i]))
					else:
						data_row.append(float(row[i]))
				x.append(data_row)
		return x,y
		
	
def splitdata(data,splitratio):
	numpy.random.shuffle(data)
	mid = int(splitratio* len(data))
	train_x = data[:mid]
	test_x = data[mid:]
	return train_x,test_x
x,y = loaddata()

Lg = GaussianNB()
Trained = Lg.fit(x, y)
predict = Trained.predict(x)

a=0
b=0
for i in range(0,len(y),1):
	if y[i] == predict[i]:
		a+=1
	else:
		b+=1
print a
print b

x, y = loaddata()