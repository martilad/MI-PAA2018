import timeit
import click
import os 
import time

from random import randint

import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from GA import ga
from time import sleep
from os import listdir
from os.path import isfile, join
from enum import Enum
def read_problem_file(file):
	n_var = 0
	n_clause = 0
	chars = file.read().split()
	print(chars)
	clause = []
	cnt = 0
	n_c = 0
	for i in chars:
		if len(i) < 1: continue
		if i[0].strip() == 'c':
			continue
		if i[0].strip() == 'p':
			ind, problem, n_v, n_c = i.split()
			if problem.lower() != 'cnf':
				print('Can\'t solve not cnf problem')
				return
			n_v = int(n_v)
			n_c = int(n_c)
			continue
		clause.append([int(j) for j in i.split()[:-1]])
		cnt += 1
		if cnt >= n_c:
			break


	return


@click.command()
@click.option('-f', '--problems', metavar='FOLDER', help="Folder with problems to solve.")
@click.option('-o', '--out', metavar='OUTSTRING', help="Out string before to create files (plots, data). Can be path.")
@click.option('-c', '--config', metavar='CONFIG', help="Config file in yaml format.")
def solve(problems, out, config):
	if os.path.isdir(problems):
		only_files = [problems + "/" + f for f in listdir(problems) if isfile(join(problems, f))]
		for file in only_files:
			f = open(file, "r")
			contents = f.readlines()
			f.close()
			index = 0
			var = 0
			for i, j in enumerate(contents):
				if j[0] == 'p':
					print(j)
					var = int(j.split()[2])
					index = int(i)

			contents.insert(index, "c weights " + " ".join([str(randint(1, 50)) for k in range(var)]) + "\n")

			f = open(file, "w")
			contents = "".join(contents)
			f.write(contents)
			f.close()
	else:
		print("Problems not a path to problems.")

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step



if __name__ == '__main__':
	solve()
