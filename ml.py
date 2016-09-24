import numpy
import math
import csv
from collections import Counter

def load_y():
	with open('Project1_data.csv', 'rb') as mycsvfile:
		thedata = csv.reader(mycsvfile)
		Processeddata = []
		number = -2

		for row in thedata:
			number+=1
			if number == -1:
				pass
			else:
	
				bool = 0

				eventdate = 1
				pos = 3
				oasispos = 2
				while pos <len(row) and oasispos <len(row):
					if row[oasispos][:14] =='Marathon Oasis' and row[pos]== 'Marathon' and row[eventdate]== '2015-09-20':
						bool = 1
					oasispos+=5
					pos+=5
					eventdate+=5
				Processeddata.append(bool)
	return Processeddata

def load_x(Listparameters):
	with open('full_data.csv', 'rb') as mycsvfile:
		thedata = csv.reader(mycsvfile)
		x = []
		y = []
		z = [] # Column
		count = 0

		for row in thedata:
			count += 1
			if count <2:
				for i in range(0,len(row),1):
					z.append(row[i]) 
			if count >=2:
				data_row = []
				for i in range(0,len(row),1):
					if z[i] == '2015-09-20':
						y.append(float(row[i]))
					elif z[i] in Listparameters:
						data_row.append(float(row[i]))
				x.append(data_row)
		return x

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

def calculateProbability(x, mean, stdev):
	if isinstance(x, basestring):
		return 1
	else:
		exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
		return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

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

def predict(x_test,y_test,summarizeddata,datasetcommand):
	t = 0
	f = 0
	ListofResults = []

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
		ListofResults.append(Highestclass)
		if Validation == Highestclass:
			t+=1
		else:
			f+=1
	return ListofResults, float(t)/(f+t) 

def K_fold_Cross_Validate(x,y,k=5):
	Testsetsize = len(x)/k
	splitBegin = 0
	splitEnd = Testsetsize
	Acclist = []
	while splitEnd <len(x):

		x_test = x[splitBegin:splitEnd]
		y_test = y[splitBegin:splitEnd]

		x_train = x[:splitBegin] +x[splitEnd:]
		y_train = y[:splitBegin] +y[splitEnd:]

		Summary = summarizeddata(x_train,y_train,datasetcommand = ['Continuous','Discrete','Continuous','Continuous','Continuous','Continuous','Continuous'])
		Result, Accuracy = predict(x_test,y_test,Summary,datasetcommand = ['Continuous','Discrete','Continuous','Continuous','Continuous','Continuous','Continuous'])
		Acclist.append(Accuracy) 
		splitEnd +=  Testsetsize
		splitBegin +=  Testsetsize
	print "when k = "+ str(k)+" cross validataion = "+ str(sum(Acclist) / float(len(Acclist)))



def K_fold_Test_Each_Data(x,y,k=5):
	f = open("Output.csv", "wt")
	Testsetsize = len(x)/k
	splitBegin = 0
	splitEnd = Testsetsize
	TrainerSummary = []
	true = 0
	false =0
	while splitEnd <len(x):
		x_train = x[:splitBegin] +x[splitEnd:]
		y_train = y[:splitBegin] +y[splitEnd:]

		Summary = summarizeddata(x_train,y_train,datasetcommand = ['Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous'])
		TrainerSummary.append(Summary)
		splitEnd +=  Testsetsize
		splitBegin +=  Testsetsize

	for i in range(0,len(x),1):
		expected_y = y[i]

		MeanOutput = []

		x_test = [x[i]]
		y_test = [y[i]]

		for trainer in TrainerSummary:
			Result, Accuracy = predict(x_test,y_test,trainer,datasetcommand = ['Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous'])
			MeanOutput.append(Result[0])
			splitEnd +=  Testsetsize
			splitBegin +=  Testsetsize

		count = Counter(MeanOutput)
		Result = count.most_common()[0][0]

		if Result == expected_y:
			true+=1
		else:
			false+=1
		f.write(str(Result))
		f.write("\n")
	print "accuracy of " +str(k)+ " fold cross validation = "+str(float(true)/(true+false))


def different_k_crossvalidation(List,X,Y):
	for k in List:
		print "when k = "+str(k)+" cross validation accuracy = :"
		K_fold_Cross_Validate(X,Y,k)

X = load_x(['marathon_ratio','sex','age','n_oasis','2014-09-28','2013-09-22','2013-02-17'])
Y = load_y()


K_fold_Test_Each_Data(X,Y,k=5)

