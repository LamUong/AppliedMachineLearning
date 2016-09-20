import load
import numpy
import math
import csv
'''
	# of marathons, # Oasis events, Sex, Age, participate in 2015-09-20 Marathon(0 = n0, 1 = yes),index

'''
def loadCsv(filename):
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

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

def summarizeddata(trainset,datasetcommand = ['Discrete','Discrete','Discrete','Continuous','Result','ID']):
	
	HashbyClass = {}
	for data in trainset:
		if data[-2] in HashbyClass:
			HashbyClass[data[-2]].append(data)
		else:
			HashbyClass[data[-2]] = []
			HashbyClass[data[-2]].append(data)
	
	HashofClasses = {}
	HashofClasses['ratio'] = {}

	for Class in HashbyClass:
		HashofClasses['ratio'][Class] = float(len(HashbyClass[Class]))/len(trainset)

	for Class in HashbyClass:
		Listofattributes = [{},{},{},{}]
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

def predict(testset,summarizeddata,datasetcommand = ['Continuous','Discrete','Discrete','Continuous','Result','ID']):
	t = 0
	f = 0
	for data in testset:
		Validation = data[4]
		hashclasspredict = {}
		for Class in summarizeddata['ratio']:
			probY = summarizeddata['ratio'][Class]
			probXgivenY = 1
			for i in range(0,len(data),1):
				if datasetcommand[i] == 'ID' or datasetcommand[i] == 'Result':
					pass
				elif datasetcommand[i] == 'Discrete':
					if i not in summarizeddata[Class]:
						pass
					else:
						print 'shitme'

						probXgivenY *= float(summarizeddata[Class][i][data[i]])/summarizeddata[Class][i]['totalcount']
				elif datasetcommand[i] == 'Continuous':
					print data[i], summarizeddata[Class][i]['avg'], summarizeddata[Class][i]['stdev']
					#print calculateProbability(data[i], summarizeddata[Class][i]['avg'], summarizeddata[Class][i]['stdev'])
					probXgivenY *= calculateProbability(data[i], summarizeddata[Class][i]['avg'], summarizeddata[Class][i]['stdev'])
					
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
	print t 
	print f
			

a = load.loaddata()


train,test = splitdata(a,0.67)

summarizeddata = summarizeddata(train,datasetcommand = ['Continuous','Discrete','Discrete','Discrete','Result','ID'])

predict(test,summarizeddata,datasetcommand = ['Continuous','Discrete','Discrete','Discrete','Result','ID'])

'''
data = loadCsv('data.csv')
train,test = splitdata(data,0.67)
summarizeddata = summarizeddata(train,
	datasetcommand = ['Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','ID'])
print summarizeddata['ratio']
predict(test,summarizeddata,datasetcommand = ['Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','Continuous','ID'])
'''