import timeit
import click
import os 
import time
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sa import sa
from time import sleep
from os import listdir
from os.path import isfile, join
from enum import Enum


"""Create file in csv format for writing stats."""
class WriteCSVData():

	def __init__(self, file, sep = ","):
		self.file = open(file, 'w')
		self.head = None
		self.sep = sep

	"""Append one line to file, if it is first line -> create header"""
	def appendLine(self, kwargs):
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


	def __init__(self, problem):
		self.max = 5000
		self.best = 0
		self.solutions = []
		if (len(problem)<2 or (len(problem[3:][1::2]) != len(problem[3:][::2])) or  (len(problem[3:][::2]) != int(problem[1]))):
			print("Solution: ", problem[0]+" " if len(problem)>0 else "", " Error format.")
			self.bad = True
			raise BaseException()
		self.n = problem[1]
		self.itemsP = problem[3:][1::2]
		self.itemsW = problem[3:][::2]
		self.itemsP = [int(x) for x in self.itemsP]
		self.itemsW = [int(x) for x in self.itemsW]
		self.maxWeight = int(problem[2])

	"""solve one instance for brute force -> method for time meansuring"""
	def knapSackBruteForce(self, n, currentPrice, currentWeight, knap):
		#if currentWeight > self.maxWeight: return
		if (n > int(self.n)-1) and (currentWeight <= self.maxWeight) and (currentPrice >= self.best):
			tmp = [currentPrice]
			tmp.append(list(knap))
			self.solutions.append(tmp)
			self.best = currentPrice
		if n > int(self.n)-1: return
		self.knapSackBruteForce(n+1, currentPrice + int(self.itemsP[n]), currentWeight + int(self.itemsW[n]), knap + "1")
		self.knapSackBruteForce(n+1, currentPrice, currentWeight, knap + "0" )
		

	"""Prepare variables for solve one instance for brute force"""
	def solveTBruteForce(self):
		self.solutions = []
		self.knapSackBruteForce(0, 0, 0, "")

	def knapSackBranchAndBound(self, n, currentPrice, currentWeight, knap):
		#print(self.itemsP[:len(self.itemsP) - len(knap)], knap)
		if currentPrice + sum(self.itemsP[len(knap):]) < self.best: return
		if currentWeight > self.maxWeight: return
		if (n > int(self.n)-1) and (currentWeight <= self.maxWeight) and (currentPrice >= self.best):
			tmp = [currentPrice]
			tmp.append(list(knap))
			self.solutions.append(tmp)
			self.best = currentPrice
		if n > int(self.n)-1: return
		self.knapSackBranchAndBound(n+1, currentPrice + int(self.itemsP[n]), currentWeight + int(self.itemsW[n]),  knap + "1")
		self.knapSackBranchAndBound(n+1, currentPrice, currentWeight, knap + "0" )
		

	"""Prepare variables for solve one instance for brute force"""
	def solveTBranchAndBound(self):
		self.solutions = []
		self.knapSackBranchAndBound(0, 0, 0, "")

	"""dynamic decomposition by weight"""
	def knapSackDynamicWeight(self, n, currentPrice, currentWeight, knap):
		if currentWeight > self.maxWeight: return

		if self.weightTable[n][currentWeight] > currentPrice: return
		self.weightTable[n][currentWeight] = currentPrice

		if (n > int(self.n)-1) and (currentPrice >= self.best[0]):
			self.best = [currentPrice, currentWeight, n]
		if n > int(self.n)-1: return

		self.knapSackDynamicWeight(n+1, currentPrice + int(self.itemsP[n]), currentWeight + int(self.itemsW[n]), knap + "1")
		self.knapSackDynamicWeight(n+1, currentPrice, currentWeight, knap + "0" )
		

	"""Prepare variables for solve one instance for brute force"""
	def solveTDynamicWeight(self):
		self.best = [0,0,0]
		self.weightTable = np.full((int(self.n)+1, self.maxWeight+1), 0)
		self.knapSackDynamicWeight(0, 0, 0, "")
		solPrice = self.best[0]
		sol = ""
		while(True):
			if self.weightTable[self.best[2]-1][self.best[1]] != self.weightTable[self.best[2]][self.best[1]]:
				sol = "1" + sol
				self.best[1] = self.best[1] - self.itemsW[self.best[2]-1]
				self.best[0] = self.best[0] - self.itemsP[self.best[2]-1]
			else:
				sol = "0" + sol
			self.best[2] = self.best[2] - 1
			if self.best[2] == 0: break
		self.solutions = [[solPrice, list(sol)]]

	"""dynamic decomposition by cost"""
	def knapSackDynamicPrice(self, n, currentPrice, currentWeight, knap):

		if currentWeight > self.maxWeight: return

		if self.priceTable[n][currentPrice] < currentWeight: return
		self.priceTable[n][currentPrice] = currentWeight

		if (n > int(self.n)-1) and (currentPrice >= self.best[0]):
			self.best = [currentPrice, currentWeight, n]
		if n > int(self.n)-1: return
		self.knapSackDynamicPrice(n+1, currentPrice + int(self.itemsP[n]), currentWeight + int(self.itemsW[n]), knap + "1")
		self.knapSackDynamicPrice(n+1, currentPrice, currentWeight, knap + "0" )
		

	"""Prepare variables for solve one instance for brute force"""
	def solveTDynamicPrice(self):
		self.best = [0,0,0]
		self.priceTable = np.full((int(self.n)+1, sum(self.itemsP[:])+1), np.inf)
		self.knapSackDynamicPrice(0, 0, 0, "")
		solPrice = self.best[0]
		sol = ""
		while(True):
			if self.priceTable[self.best[2]-1][self.best[0]] != self.priceTable[self.best[2]][self.best[0]]:
				sol = "1" + sol
				self.best[0] = self.best[0] - self.itemsP[self.best[2]-1]
				self.best[1] = self.best[1] - self.itemsW[self.best[2]-1]
			else:
				sol = "0" + sol
			self.best[2] = self.best[2] - 1
			if self.best[2] == 0: break
		self.solutions = [[solPrice, list(sol)]]

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
		self.solutions = [tmp]

	def solveTPriceWeight(self):
		self.values = []
		self.solutions = []
		for i in range(int(self.n)):
			self.values.append([i, float(self.itemsP[i])/float(self.itemsW[i])])
		self.values = sorted(self.values, key=lambda sol: sol[1])[::-1]
		self.sol = [0 for x in range(int(self.n))]
		self.knapSackHPriceWeight(self.values)

	def knapSackFPTAS(self, n, currentPrice, currentWeight, knap):
		if currentWeight > self.maxWeight: return

		if self.priceTable[n][currentPrice] < currentWeight: return
		self.priceTable[n][currentPrice] = currentWeight

		if (n > int(self.n)-1) and (currentPrice >= self.best[0]):
			self.best = [currentPrice, currentWeight, n]
		if n > int(self.n)-1: return
		self.knapSackFPTAS(n+1, currentPrice + int(self.itemsPF[n]), currentWeight + int(self.itemsW[n]), knap + "1")
		self.knapSackFPTAS(n+1, currentPrice, currentWeight, knap + "0" )

	def solveTPFPTAS(self, e):
		self.best = [0,0,0]
		maxCost = max(self.itemsP[:])
		k  = (maxCost * e) / int(self.n)
		self.itemsPF = [int(i / k) for i in self.itemsP]
		self.priceTable = np.full((int(self.n)+1, sum(self.itemsPF[:])+1), np.inf)
		self.knapSackFPTAS(0, 0, 0, "")
		solPrice = 0
		sol = ""
		while(True):
			if self.priceTable[self.best[2]-1][self.best[0]] != self.priceTable[self.best[2]][self.best[0]]:
				sol = "1" + sol
				solPrice += self.itemsP[self.best[2]-1]
				self.best[0] = self.best[0] - self.itemsPF[self.best[2]-1]
				self.best[1] = self.best[1] - self.itemsW[self.best[2]-1]
			else:
				sol = "0" + sol
			self.best[2] = self.best[2] - 1
			if self.best[2] == 0: break
		self.solutions = [[solPrice, list(sol)]]


	"""Prepare variables for solve one instance heuristic price/weight"""
	def solve(self, ENUM, *args):
		t = self.timeMensure(ENUM, 1, self, *args)
		t = self.timeMensure(ENUM, ((int)(self.max / t) if (int)(self.max / t) > 0 else 1), self, *args)
		sor = sorted(self.solutions, key=lambda sol: sol[0])[::-1]
		if (len(sor)>0):
			self.solutions = [x for x in sor if x[0] == sor[0][0]]
		return self.solutions, t

	"""Time mensure function for get cpu average time in specific count of run"""
	def timeMensure(self, function, count, *args):
		self.solutions = []
		self.best = 0
		time = timeit.timeit(functools.partial(function, *args), number=count)
		return (time/count)*1000

class ALG(Enum):
	HPW = KnapSackSolver.solveTPriceWeight
	BT = KnapSackSolver.solveTBruteForce
	BB = KnapSackSolver.solveTBranchAndBound
	DC = KnapSackSolver.solveTDynamicPrice
	DW = KnapSackSolver.solveTDynamicWeight
	FPTAS = KnapSackSolver.solveTPFPTAS

"""Load problem from file. 
	Format: ID n, M, weight, price, ...."""
def loadProblemFromFile(fileName):
	with open(fileName, 'r') as f:
		return loadProblemFromOpenFile(f)

"""Load problem from open file. 
	Format: ID n, M, weight, price, ...."""
def loadProblemFromOpenFile(fileName):
	return [x.strip()[0:].split(" ") for x in fileName.readlines()]

def printInlineSolutions(ID, n, solution):
	ret = ""
	for i in solution:
		ret += ID + " " + n +  " " + str(i[0]) 
		for j in i[1]:
			ret = ret + " " + j
		ret += "\n"
	return ret[0:-1]

@click.group()
def my_knap_sack_solver():
	pass

"""Namage function fo subcommand solve. Solve one problem get inline or probles in one file. Use brutforce and print stats to terminal."""
@my_knap_sack_solver.command()
@click.option('-f', '--file', type=click.File(), metavar='file', help="File with problem. When is specific file, the inline solution will not be solve.")
@click.argument('ins', nargs=-1, metavar="inline solution")
def solve(file, ins):
	try:
		if file is None and len(ins)>2:
			print(printInlineSolutions(ins[0], ins[1], KnapSackSolver(ins).solveTBruteForce()[0]))
			return
		elif file is not None:
			problems = loadProblemFromOpenFile(file)
			for i in problems:
				print(printInlineSolutions(i[0], i[1], KnapSackSolver(i).solveTBruteForce()[0]))
			return
	except BaseException as e:
		raise e
		return
	print("Error - problem format")

"""	Solve and test and stats instances with simulated anealing"""
@my_knap_sack_solver.command()
@click.option('--outfile', help="prefix for outfile, to outfile will be printed data from\
	simulated annealing and with some suffing created plot", required=True)
@click.option('-g', is_flag=True)
@click.option('-f', '--file', type=click.File(), help="File with problem or problems to solve by simulated anealing.", required=True)
def SA(outfile, g, file):
	if file is not None:
		problems = loadProblemFromOpenFile(file)
		for i in problems:
			t1 = time.time()
			result, sollution, plot = sa(i, 400, 0.997, 1, 40)
			t = time.time() - t1
			test = pd.DataFrame(plot)
			test.columns = ['temp', "best", "current"]
			test = test[::-1]
			test.index = test['temp']
			test = test.drop('temp', axis=1)
			pie = test.plot()
			pie.invert_xaxis()
			fig = pie.get_figure()
			fig.savefig("myplot.pdf")
			print(result)

	

"""	Manage function for subcommand stats. Compering algorithm to brute force count time and relative error. 
	Can list whole directory with instance of problem or one file"""
@my_knap_sack_solver.command()
@click.option('--outfile', help="", required=True)
@click.option('-b', is_flag=True)
@click.option('-h', is_flag=True)
@click.option('-bb', is_flag=True)
@click.option('-dc', is_flag=True)
@click.option('-dw', is_flag=True)
@click.option('-fptas', help="Values of epsilon to test separate by comma.")
@click.option('-p', '--path', help="Path to files or file with sollution to do time mensuring.", required=True)
def stats(outfile, b, h, bb, dc, dw, fptas, path):
	if (b or bb or dc or dw) == False:
		print("Není zadán Exaktní algoritmus, u aproximativních nebude měřena relativní chyba.")
	csv = WriteCSVData(outfile, ",")
	if os.path.isdir(path):
		onlyFiles = [path+"/"+f for f in listdir(path) if isfile(join(path, f))]
		if len(onlyFiles) == 0:
			exit(0)
		sortOnlyFiles = [(onlyFiles[0].split('_')[0] + "_" + str(y) + "." + ".".join(("_".join(onlyFiles[0].split('_')[1:])).split(".")[1:]))  # do join file name back after sort by numbers
					for y in sorted(int(x.split(".")[0]) # remove name before number
					for x in (i.split("_")[-1] for i in onlyFiles))] # remove name after number
		for file in sortOnlyFiles:
			prices = loadProblemFromFile(file)
			for i in prices:
				try:
					solve(csv, i, b, h, bb, dc, dw, fptas)
				except Exception as e:
					raise e
					continue
				
	elif os.path.isfile(path):  
		prices = loadProblemFromFile(path)
		for i in prices:
			try:
				solve(csv, i, b, h, bb, dc, dw, fptas)
			except Exception as e:
				raise e
				continue
	else:  
		print("Not a valid directory or file." )
		exit()

def brut_run(err, brut, brutOK, tmp):
	err = True
	if brut is None: brut = tmp
	else:
		if brut != tmp:
			brutOK = False
	return err, brut, brutOK

def error(sol, best):
	return (best - sol)/best


"""Function for solve one instance of problem and write stats to the csv file."""
def solve(file, ins, b, h, bb, dc, dw, fptas):
	kwargs = {}
	kwargs['n'] = ins[1]
	err = False
	brut = None
	brutOK = True
	if b:
		tmp, tB = KnapSackSolver(ins).solve(ALG.BT)
		err, brut, brutOK = brut_run(err, brut, brutOK, tmp[0][0])
		kwargs['tB'] = tB 
	if bb:
		tmp, tBB = KnapSackSolver(ins).solve(ALG.BB)
		err, brut, brutOK = brut_run(err, brut, brutOK, tmp[0][0])
		kwargs['tBB'] = tBB
	if dc:
		tmp, tDC = KnapSackSolver(ins).solve(ALG.DC)
		err, brut, brutOK = brut_run(err, brut, brutOK, tmp[0][0])
		kwargs['tDC'] = tDC
	if dw:
		tmp, tDW = KnapSackSolver(ins).solve(ALG.DW)
		err, brut, brutOK = brut_run(err, brut, brutOK, tmp[0][0])
		kwargs['tDW'] = tDW
	if h:
		tmp, tH = KnapSackSolver(ins).solve(ALG.HPW)
		kwargs['tH'] = tH
		if err: kwargs['errH'] = error(tmp[0][0], brut)
	if fptas:
		for i in [float(s) for s in fptas.split(',')]:
			tmp, tFPTAS = KnapSackSolver(ins).solve(ALG.FPTAS, i)
			kwargs['tFPTASeps'+str(i)] = tFPTAS
			if err: kwargs['errFPTASeps'+str(i)] = error(tmp[0][0], brut)
	kwargs['err'] = err
	kwargs['brutOK'] = brutOK
	file.appendLine(kwargs)

if __name__ == '__main__':
	my_knap_sack_solver()
