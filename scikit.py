from sklearn import datasets
iris = datasets.load_iris()
from sklearn.naive_bayes import GaussianNB
import load

gnb = GaussianNB()

wholedata = load.loaddata()

x = []
y = []
for data in wholedata:
	x.append(data[:-1])
	y.append(data[-1])





y_pred = gnb.fit(x, y).predict(x)
a = 0
b = 0
for y1,y2 in zip(y_pred,y):
	if y1==y2:
		a+=1
	else:
		b+=1
print a
print b