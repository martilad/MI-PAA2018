import timeit
import click
import os 
import functools
import numpy as np

from time import sleep
from os import listdir
from os.path import isfile, join

"""Create file in csv format for writing stats."""
class WriteCSVData():

	def __init__(self, file, sep = ","):
		self.file = open(file, 'w')
		self.head = None
		self.sep = sep

	"""Append one line to file, if it is first line -> create header"""
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
		self.file.flush()
		
"""Solver class for one knapSack problem"""
class KnapSackSolver:

	def __init__(self, problem, repeatB, repeatH):
		self.best = 0
		self.solutions = []
		if (len(problem)<2 or (len(problem[3:][1::2]) != len(problem[3:][::2])) or  (len(problem[3:][::2]) != int(problem[1]))):
			print("Solution: ", problem[0]+" " if len(problem)>0 else "", " Error format.")
			self.bad = True
			return
		self.n = problem[1]
		self.repeatB = repeatB
		self.repeatH = repeatH
		self.itemsP = problem[3:][1::2]
		self.itemsW = problem[3:][::2]
		self.maxWeight = int(problem[2])

	"""solve one instance for brute force -> method for time meansuring"""
	def knapSackBruteForce(self, n, currentPrice, currentWeight, knap):
		if currentWeight > self.maxWeight: return
		if n == -1 and currentWeight <= self.maxWeight and currentPrice >= self.best:
			tmp = [currentPrice]
			tmp.append(list(knap))
			self.solutions.append(tmp)
			self.best = currentPrice
		if n == -1: return
		self.knapSackBruteForce(n-1, currentPrice, currentWeight, "0" + knap )
		self.knapSackBruteForce(n-1, currentPrice + int(self.itemsP[n]), currentWeight + int(self.itemsW[n]), "1" + knap)

	"""solve one instance for heuristic price/weight -> method for time meansuring"""
	def knapSackHPriceWeight(self, priceWeight):
		weight = 0
		price = 0
		for index, priceW in priceWeight:
			if weight + int(self.itemsW[index]) > self.maxWeight:
				continue
			self.sol[index] = 1
			weight += int(self.itemsW[index])
			price += int(self.itemsP[index])
		tmp = [price]
		tmp.append(self.sol)
		self.solut = tmp

	"""Prepare variables for solve one instance for brute force"""
	def solveTBruteForce(self):
		self.solutions = []
		t = self.timeMensure(KnapSackSolver.knapSackBruteForce, self.repeatB, self, int(self.n)-1, 0, 0, "" )
		sor = sorted(self.solutions, key=lambda sol: sol[0])[::-1]
		if (len(sor)>0):
			self.solutions = [x for x in sor if x[0] == sor[0][0]]
		return self.solutions, t

	"""Prepare variables for solve one instance heuristic price/weight"""
	def solveTPriceWeight(self):
		self.values = []
		for i in range(int(self.n)):
			self.values.append([i, float(self.itemsP[i])/float(self.itemsW[i])])
		self.values = sorted(self.values, key=lambda sol: sol[1])[::-1]
		self.sol = [0 for x in range(int(self.n))]
		t = self.timeMensure(KnapSackSolver.knapSackHPriceWeight,self.repeatH, self, self.values)
		return self.solut, t
	
	"""Solve brute force and heuristic and compute time for both and and return relative error (opt-heu)/opt"""
	def solveBothWithError(self):
		sol, tH = self.solveTPriceWeight()
		solution, tB = self.solveTBruteForce()
		return solution, tH, tB, (solution[0][0]-sol[0])/solution[0][0]

	"""Time mensure function for get cpu average time in specific count of run"""
	def timeMensure(self, function, count, *args):
		time = timeit.timeit(functools.partial(function, *args), number=count)
		return (time/count)*1000


"""Load problem from file. 
	Format: ID n, M, weight, price, ...."""
def loadProblemFromFile(fileName):
	with open(fileName, 'r') as f:
		return loadProblemFromOpenFile(f)

"""Load problem from open file. 
	Format: ID n, M, weight, price, ...."""
def loadProblemFromOpenFile(fileName):
	return [x[0:-1].split(" ") for x in fileName.readlines()]

def printInlineSolutions(ID, n, solution):
	ret = ""
	for i in solution:
		ret += ID + " " + n +  " " + str(i[0]) 
		for j in i[1]:
			ret = ret + " " + j
		ret += "\n"
	return ret[0:-1]

@click.group()
def my_git():
	pass

"""Namage function fo subcommand solve. Solve one problem get inline or probles in one file. Use brutforce and print stats to terminal."""
@my_git.command()
@click.option('-f', '--file', type=click.File(), metavar='file', help="File with solutions. When is specific file, the inline solution will not be solve.")
@click.argument('ins', nargs=-1, metavar="inline solution")
def solve(file, ins):
	if file is None:
		print(printInlineSolutions(ins[0], ins[1], KnapSackSolver(ins, 1).solveTBruteForce()[0]))
		return
	problems = loadProblemFromOpenFile(file)
	for i in problems:
		print(printInlineSolutions(i[0], i[1], KnapSackSolver(i, 1).solveTBruteForce()[0]))

"""	Manage function for subcommand stats. Compering algorithm to brute force count time and relative error. 
	Can list whole directory with instance of problem or one file"""
@my_git.command()
@click.option('-o', '--outfile', help="", required=True)
@click.option('-t', '--time', is_flag=True)
@click.option('-e', '--error', is_flag=True)
@click.option('-rb', '--repeatB', help="How many times repeat time mensure for brute force to get average on one solution.", type=int, default=1)
@click.option('-rh', '--repeatH', help="How many times repeat time mensure for heuristic to get average on one solution.", type=int, default=1000)
@click.option('-p', '--path', help="Path to files or file with sollution to do time mensuring.", required=True)
def stats(outfile, time, error, repeatb, repeath, path):
	csv = WriteCSVData(outfile, ",")
	if os.path.isdir(path):  
		onlyFiles = ["testInst/"+f for f in listdir("testInst") if isfile(join("testInst", f))]
		sortOnlyFiles = [(onlyFiles[0].split('_')[0] + "_" + str(y) + "." + ".".join(onlyFiles[0].split('.')[1:])) # do join file name back after sort by numbers
					for y in sorted(int(x.split("_")[1]) # remove name before number
					for x in (i.split(".")[0] for i in onlyFiles))] # remove name after number
		for file in sortOnlyFiles:
			prices = loadProblemFromFile(file)
			for i in prices:
				solve(csv, i, repeatb, repeath, time, error)
				
	elif os.path.isfile(path):  
		prices = loadProblemFromFile(path)
		for i in prices:
			solve(csv, i, repeatb, repeath, time, error)
	else:  
		print("Not a valid directory or file." )
		exit()

"""Function for solve one instance of problem and write stats to the csv file."""
def solve(file, ins, repeatb, repeath, time, error):
	if error:
		sollution, tH, tB, e = KnapSackSolver(ins, repeatb, repeath).solveBothWithError()
		file.appendLine(n=ins[1], error=e, timeBrut=tB, timeHeu = tH, repeatB=repeatb, repeatH = repeath)
		return
	if time:
		sollution, t = KnapSackSolver(ins, repeatb, repeath).solveTBruteForce()
		file.appendLine(n=ins[1], time=t, repeatB=repeatb, repeatH = repeath)
		return

if __name__ == '__main__':
	my_git()
