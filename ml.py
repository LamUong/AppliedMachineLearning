import load
import numpy
import math
import csv
def mean(List):
	count = 0
	sum = 0
	for number in List:
		if not isinstance(number, basestring):
			sum += number
			count += 1
	return sum/float(count), count

def returnAverageandStandarddeviation(List):
	avg, count = mean(List)
	variance = sum([pow(x-avg,2) for x in List if not isinstance(x, basestring)])/float(count)
	return avg, math.sqrt(variance)

def splitdata(data,splitratio):
	numpy.random.shuffle(data)
	mid = int(splitratio* len(data))
	train_x = data[:mid]
	test_x = data[mid:]
	return train_x,test_x

def summarizeddata(X_train,Y_train,datasetcommand):
	
	HashbyClass = {}
	for x,y in zip(X_train,Y_train):
		if y in HashbyClass:
			HashbyClass[y].append(x)
		else:
			HashbyClass[y] = []
			HashbyClass[y].append(x)
	
	HashofClasses = {}
	HashofClasses['ratio'] = {}

	for Class in HashbyClass:
		HashofClasses['ratio'][Class] = float(len(HashbyClass[Class]))/len(X_train)

	for Class in HashbyClass:

		Listofattributes = []
		for attr in X_train:
			Listofattributes.append({}) 

		for data in HashbyClass[Class]:
			for i in range(0,len(data),1):
				if datasetcommand[i] == 'ID' or datasetcommand[i] == 'Result':
					pass

				elif datasetcommand[i] == 'Discrete':
					if data[i] not in Listofattributes[i]:
						Listofattributes[i][data[i]] = 1
					else:
						Listofattributes[i][data[i]] +=1

				elif datasetcommand[i] == 'Continuous':
					if 'list' not in Listofattributes[i]:
						Listofattributes[i]['list'] = []
						Listofattributes[i]['list'].append(data[i])
					else:
						Listofattributes[i]['list'].append(data[i])

		for attribute in Listofattributes:
			if 'list' in attribute:
				avg, stv = returnAverageandStandarddeviation(attribute['list'])
				attribute['avg'] = avg
				attribute['stdev'] = stv
			else:
				totalcount = 0
				for category in attribute:
					totalcount += attribute[category]
				attribute['totalcount'] = totalcount
		HashofClasses[Class] = Listofattributes

	return HashofClasses

def calculateProbability(x, mean, stdev):
	if isinstance(x, basestring):
		return 1
	else:
		exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
		return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def predict(x_test,y_test,summarizeddata,datasetcommand):
	t = 0
	f = 0
	for x, y in zip(x_test,y_test):
		Validation = y

		hashclasspredict = {}

		for Class in summarizeddata['ratio']:
			probY = summarizeddata['ratio'][Class]
			probXgivenY = 1

			for i in range(0,len(x),1):
				if datasetcommand[i] == 'ID' or datasetcommand[i] == 'Result':
					pass
				elif datasetcommand[i] == 'Discrete':
					probXgivenY *= float(summarizeddata[Class][i][x[i]])/summarizeddata[Class][i]['totalcount']
				elif datasetcommand[i] == 'Continuous':
					probXgivenY *= calculateProbability(x[i], summarizeddata[Class][i]['avg'], summarizeddata[Class][i]['stdev'])	
			
			totalprob = probY* probXgivenY
			hashclasspredict[Class] = totalprob

		Prediction = 0
		for Class in hashclasspredict:
			if hashclasspredict[Class] > Prediction:
				Prediction = hashclasspredict[Class]
				Highestclass = Class
		if Validation == Highestclass:
			t+=1
		else:
			f+=1
	print float(t)/(f+t) 

def loaddata(Listparameters):
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
					elif i in Listparameters:
						data_row.append(float(row[i]))
				x.append(data_row)
		return x,y,z

import csv
Listparameters = []
with open('NaieveBayes.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	Listparameters.append(row[1])



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

x,y,z = loaddata(Listparameters)




x_train = x[:6000]
x_test = x[6000:]
y_train = y[:6000]
y_test = y[6000:]
summarizeddata = summarizeddata(x_train,y_train,datasetcommand = ['Continuous','Discrete','Continuous','Continuous','Continuous','Continuous','Continuous'])

predict(x_test,y_test,summarizeddata,datasetcommand = ['Continuous','Discrete','Continuous','Continuous','Continuous','Continuous','Continuous'])
	# of marathons, #Oasisevents, RatioOasis/Allevents, Sex, Age, participate in 2015-09-20 Marathon(0 = n0, 1 = yes),ID
