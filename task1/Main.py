import timeit
from time import sleep
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
		
def test():
	"-".join(str(n) for n in range(100))

def timeMensure(function, count):
	time = timeit.timeit(function, number=count)
	return (time/count)*1000

if __name__ == '__main__':
	print("Test for 1000 loop in ", timeMensure(function=test, count=1000), " ms.")
	write = WriteCSVData("test")
	write.appendLine(n=50, name=10, zeta="lol")
	onlyfiles = [f for f in listdir("testInst") if isfile(join("testInst", f))]
	print(onlyfiles)


