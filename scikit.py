from sklearn.linear_model import LogisticRegression
import load
import numpy
def splitdata(data,splitratio):
	numpy.random.shuffle(data)
	mid = int(splitratio* len(data))
	train_x = data[:mid]
	test_x = data[mid:]
	return train_x,test_x

Lg = LogisticRegression()

wholedata = load.loaddata()
train,test = splitdata(wholedata,0.67)

x = []
y = []
# of marathons, #Oasisevents, RatioOasis/Allevents, Sex, Age, participate in 2015-09-20 Marathon(0 = n0, 1 = yes),ID
for data in train:
	x.append(data[:5])
	y.append(data[-2])
print x[1]
print y[1]

x_test = []
y_test = []
for data in test:
	x_test.append(data[:5])
	y_test.append(data[-2])

Trained = Lg.fit(x, y)
predict = Trained.predict(x_test)
print predict 
a=0
b=0
for i in range(0,len(y_test),1):
	if y_test[i] == predict[i]:
		a+=1
	else:
		b+=1
print a
print b