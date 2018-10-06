import timeit
from time import sleep
import numpy as np
from os import listdir
from os.path import isfile, join

class WriteCSVData():

	def __init__(self, file, sep = ","):
		self.file = open(file, 'w')
		self.head = None
		self.sep = sep

	def appendLine(self, **kwargs):
		if self.head is not None:
			self.writeLine(kwargs=kwargs)
		else:
			self.writeHead(kwargs)
			self.writeLine(kwargs)

	def writeHead(self, kwargs):
		self.head = []
		for key in kwargs:
			self.head.append(key)
		self.file.write(self.sep.join([str(key) for key in self.head]) + "\n")

	def writeLine(self, kwargs):
		self.file.write(self.sep.join([str(kwargs[key]) for key in self.head]) + "\n")
		
def knapSackBruteForce(solutions, best, itemsP, itemsW, n, maxWeight, currentPrice, currentWeight, knap):
	if n == -1 and currentWeight <= maxWeight and currentPrice >= best:
		tmp = [currentPrice]
		tmp.append(list(knap))
		solutions.append(tmp)
		best = currentPrice
	if n == -1: return

	knapSackBruteForce(solutions, best, itemsP, itemsW, n-1, maxWeight, currentPrice, currentWeight, "0"+knap )
	knapSackBruteForce(solutions, best, itemsP, itemsW, n-1, maxWeight, currentPrice + int(itemsP[n]), currentWeight + int(itemsW[n]), "1"+knap )

def loadProblemFromFile(fileName):
	with open(fileName, 'r') as f:
		return [x[0:-1].split(" ") for x in f.readlines()]


def test():
	"-".join(str(n) for n in range(100))

def timeMensure(function, count):
	time = timeit.timeit(function, number=count)
	return (time/count)*1000

if __name__ == '__main__':
	print("Test for 1000 loop in ", timeMensure(function=test, count=1000), " ms.")
	write = WriteCSVData("test")
	write.appendLine(n=50, name=10, zeta="lol")
	onlyFiles = ["testInst/"+f for f in listdir("testInst") if isfile(join("testInst", f))]

	sortOnlyFiles = [(onlyFiles[0].split('_')[0] + "_" + str(y) + "." + ".".join(onlyFiles[0].split('.')[1:])) # do join file name back after sort by numbers
					for y in sorted(int(x.split("_")[1]) # remove name before number
					for x in (i.split(".")[0] for i in onlyFiles))] # remove name after number

	print(sortOnlyFiles)
	prices = loadProblemFromFile(sortOnlyFiles[0])
	for i in prices:
		solutions = []
		best = 0
		knapSackBruteForce(solutions, best, i[3:][1::2], i[3:][::2], int(i[1])-1, int(i[2]), 0, 0, "" )
		#print (solutions)
		print(sorted(solutions, key=lambda sol: sol[0])[::-1][0])
		
	



