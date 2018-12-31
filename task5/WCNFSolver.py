import click
import os
import yaml
import time
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GA import ga
from os import listdir
from os.path import isfile, join


def load_problem(file):
	with open(file, 'r') as file:
		to_read = []
		chars = file.read().split("\n")
		clause = []
		weights = []
		cnt = 0
		n_c = 0
		n_v = 0
		for i in chars:
			if len(i) < 1:
				continue
			sp = i.strip().split()
			if sp[0] == 'c' and len(sp) > 1 and sp[1] == 'weights':
				weights = sp[2:]
				continue
			if sp[0] == 'c':
				continue
			if sp[0] == 'p':
				ind, problem, n_v, n_c = i.split()
				if problem.lower() != 'cnf':
					print('Can\'t solve not cnf problem')
					return
				n_v = int(n_v)
				n_c = int(n_c)
				continue
			for j in sp:
				to_read.append(j)

			for j, k in enumerate(to_read):
				if k == '0':
					clause.append(to_read[:j])
					to_read = to_read[j+1:]
					cnt += 1
					break
			if cnt >= n_c:
				break
		return n_v, n_c, weights, clause


@click.command()
@click.option('-c', '--config', metavar='CONFIG', help="Config file in yaml format.")
def solve(config):
	if config is None:
		print("You need to specify a configuration file.")
	config = load_config(config)
	if os.path.isdir(config['in']):
		only_files = [config['in'] + "/" + f for f in listdir(config['in']) if isfile(join(config['in'], f))]
		for file in only_files:
			# load problem from file
			problem = load_problem(file)
			print(problem)
			for genSize in drange(*config['generationcount']):
				for genCount in drange(*config['generationsize']):
					for mut in drange(*config['mutation']):
						for cross in drange(*config['crossover']):
							t1 = time.time()
							data = ga(*problem, genCount, genSize, mut, cross, config['elitism'], config['selection'])
							t1 = time.time() - t1
							print(t1)
							print(data)
							# Some plots
	else:
		print("Problems not a path to problems.")


def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step


def load_config(configuration_file):
	config = {}
	with open(configuration_file, 'r') as configuration:
		cfg = yaml.load(configuration)
	if 'RUN' in cfg:
		tmp = cfg['RUN']
		if "out" in tmp:
			config['out'] = tmp['out']
		else:
			config['out'] = "out"
		if "in" in tmp:
			config['in'] = tmp['in']
		else:
			print("No inst to solve.")
			exit(1)
	else:
		print("Configuration fail. See example.")
		exit(1)
	if 'GA' in cfg:
		tmp = cfg['GA']
		for i in ['generationsize', 'generationcount', 'mutation', 'crossover']:
			if i in tmp:
				if type(tmp[i]) is int or type(tmp[i]) is float:
					config[i] = [tmp[i], tmp[i] + 1, 2]
					continue
				s = tmp[i].split()
				if len(s) == 3:
					config[i] = [float(s[0]), float(s[1]), float(s[2])]
					continue
				print("Bad values", i, "please repair in config.")
				exit(1)
			else:
				print("Not specific", i, "please add to config.")
				exit(1)
		if 'selection' in tmp:
			if tmp['selection'] == 'roulette':
				config['selection'] = 'roulette'
			else:
				config['selection'] = 'tournament'
		else:
			config['selection'] = 'tournament'
		if 'elitism' in tmp:
			if tmp['elitism']:
				config['elitism'] = True
			else:
				config['elitism'] = False
		else:
			config['elitism'] = True
	else:
		print("Configuration fail. See example.")
		exit(1)
	return config


if __name__ == '__main__':
	solve()
