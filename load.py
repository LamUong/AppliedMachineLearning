import numpy
import csv 
import re
import sys
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

