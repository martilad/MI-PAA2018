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


"""Base function for start genetic algorithm."""
@click.command()
@click.option('-f', '--file', type=click.File(), metavar='file', help="File with problem. When is specific file, the inline solution will not be solve.")
@click.argument('ins', nargs=-1, metavar="inline solution")
def solve(file, ins):
	try:
		if file is None and len(ins)>2:
			print(printInlineSolutions(ins[0], ins[1], KnapSackSolver(ins).solve(ALG.DC)[0]))
			return
		elif file is not None:
			problems = loadProblemFromOpenFile(file)
			for i in problems:
				print(printInlineSolutions(i[0], i[1], KnapSackSolver(i).solve(ALG.DC)[0]))
			return
	except BaseException as e:
		raise e
		return
	print("Error - problem format")

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step



if __name__ == '__main__':
	my_knap_sack_solver()
