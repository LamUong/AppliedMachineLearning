import numpy
import csv 
import re
import sys
def loaddata():
	with open('Project1_data.csv', 'rb') as mycsvfile:
		thedata = csv.reader(mycsvfile)
		Processeddata = []
		number = -2

		for row in thedata:
			number+=1
			if number == -1:
				pass
			else:
				Marathon = 0
				Oasis = 0
				towrite = []
				

				pos = 3
				oasispos = 2

				while pos <len(row):
					if row[pos] == 'Marathon':
						Marathon+=1
					pos+=5

				while oasispos <len(row):
					if row[oasispos][:14] =='Marathon Oasis':
						Oasis+=1
					oasispos+=5	


				bool = 0

				NoOfEvents = 0
				eventpos = 3

				while eventpos <len(row):
					NoOfEvents+=1
					eventpos+=5

				RatioNoOfOasisByAllEvents = float(Oasis)/NoOfEvents

				towrite.append(Marathon)
				towrite.append(Oasis)
				towrite.append(RatioNoOfOasisByAllEvents)

				eventdate = 1
				pos = 3
				oasispos = 2
				while pos <len(row) and oasispos <len(row):
					if row[oasispos][:14] =='Marathon Oasis' and row[pos]== 'Marathon' and row[eventdate]== '2015-09-20':
						bool = 1
					oasispos+=5
					pos+=5
					eventdate+=5


				if len(row) <5: 
					towrite.append(1)
					towrite.append(30)
				elif len(row) >=6:
					if row[5] == '':
						towrite.append(1)
						towrite.append(40)

					else:
						if row[5][0] =='M':
							towrite.append(1)
						elif row[5][0] =='F':
							towrite.append(2)
						else:
							towrite.append(1)


						numbers = row[5][1:].split("-")
						if len(numbers) ==2:
						
							a = numbers[0]
							b = numbers[1]
							if a.isdigit() and b.isdigit():
								mean = (int(a)+int(b))/2
								towrite.append(mean)
							else:	
								towrite.append(40)
						else:
							towrite.append(40)

				towrite.append(bool)
				towrite.append(row[0])
				Processeddata.append(towrite)
			
	return Processeddata



