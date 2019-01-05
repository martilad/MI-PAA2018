import click
import os
import yaml
import time
import pandas as pd
import matplotlib.pyplot as plt
from GA import ga
from os import listdir
from os.path import isfile, join


@click.command()
@click.option('-c', '--config', metavar='CONFIG', help="Config file in yaml format.")
def solve(config):
    """Method solve each problem with all parameters specific in configuration file."""
    if config is None:
        print("You need to specify a configuration file.")
    config = load_config(config)
    csv = WriteCSVData(config['out'] + "_data" + ".csv", ",")
    inst_id_counter = 0
    if os.path.isdir(config['in']):
        only_files = [config['in'] + "/" + f for f in listdir(config['in']) if isfile(join(config['in'], f))]
        for file in only_files:
            problem = load_problem(file)
            for gen_count in drange(*config['generationcount']):
                for gen_size in drange(*config['generationsize']):
                    for mut in drange(*config['mutation']):
                        for cross in drange(*config['crossover']):
                            for t_size in drange(*config['selection']):
                                t1 = time.time()
                                score, generations, n_sol, n_clau = ga(*problem, gen_count, gen_size, mut,
                                                                       cross, t_size, config['elitism'],
                                                                       config['selection_add'], config['fitness'])
                                csv.append_line({"id": inst_id_counter, "gen_size": gen_size, "gen_count": gen_count,
                                                 "mut": mut, "cross": cross, "elitism": config['elitism'],
                                                 "t_size": t_size, "time": time.time() - t1, "score": score})


                                # Solutions plot
                                fig = plt.figure()
                                ax = fig.add_subplot(1, 1, 1)
                                ax.scatter([j for j in range(gen_count)], y=n_sol, s=10, marker='^', c='red')
                                ax.set_ylabel("Počet řešení")
                                ax.set_xlabel("Generace")
                                ax.set_ylim([0, gen_size])
                                fig.savefig(config['out'] + str(inst_id_counter) + "_" + file.split("/")[-1] + "_sol" + ".pdf")
                                plt.close(fig)

                                # Generations plots with fitnes and satisfied clause
                                some_plot(n_clau, config['out'] + str(inst_id_counter) + "_" + file.split("/")[-1] + "_cla" + ".pdf", "Počet splněných clausulí")
                                some_plot(generations, config['out'] + str(inst_id_counter) + "_" + file.split("/")[-1] + "_gen" + ".pdf",
                                          "Fitness")
                                inst_id_counter += 1
    else:
        print("Problems not a path with problems.")


def some_plot(data, name, y_label):
    test = pd.DataFrame(data)
    test['max'] = test.max(axis=1)
    test['mean'] = test.mean(axis=1)
    test['median'] = test.median(axis=1)
    test['min'] = test.min(axis=1)
    test['max_x'] = test['min']
    max_x = 0
    for i in test.index:
        if test['max'][i] > max_x:
            test.loc[i, 'max_x'] = test['max'][i]
            max_x = test['max'][i]
        else:
            test.loc[i, 'max_x'] = test['max_x'][i - 1]

    fig = plt.figure(figsize=(9, 6.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(test['max'])
    ax.plot(test['mean'])
    ax.plot(test['median'])
    ax.plot(test['min'])
    ax.plot(test['max_x'])
    ax.legend(['max in generation', 'mean', 'median', 'minimum', 'maximum from begin'],
              bbox_to_anchor=(0., 1.02, 1., .102), fontsize=10, ncol=2,
              loc='lower left', mode="expand", borderaxespad=0.)
    ax.set_ylabel(y_label)
    ax.set_xlabel("Generation")
    # ax.set_ylim([0, gen_size])
    fig.savefig(name)
    plt.close(fig)


def load_problem(file):
    """Load problem form file in DIMACS format use weights in comments."""
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
                    to_read = to_read[j + 1:]
                    cnt += 1
                    break
            if cnt >= n_c:
                break
        return n_v, n_c, weights, clause


def drange(start, stop, step):
    """Range for double values."""
    r = start
    while r < stop:
        yield r
        r += step


class WriteCSVData:
    """Create file in csv format for writing stats."""

    def __init__(self, file, sep=","):
        self.file = open(file, 'w')
        self.head = None
        self.sep = sep

    """Append one line to file, if it is first line -> create header"""

    def append_line(self, kwargs):
        if self.head is not None:
            self.write_line(kwargs)
        else:
            self.write_head(kwargs)
            self.write_line(kwargs)

    def write_head(self, kwargs):
        self.head = []
        for key in kwargs:
            self.head.append(key)
        self.file.write(self.sep.join([str(key) for key in self.head]) + "\n")

    def write_line(self, kwargs):
        self.file.write(self.sep.join([str(kwargs[key]) for key in self.head]) + "\n")
        self.file.flush()


def load_config(configuration_file):
    """Load configuration from configuration file for one experimental run."""
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
        for i in ['generationsize', 'generationcount', 'mutation', 'crossover', 'selection']:
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
        if 'elitism' in tmp:
            config['elitism'] = int(tmp['elitism'])
        else:
            config['elitism'] = 0
        if 'selection_add' in tmp:
            config['selection_add'] = int(tmp['selection_add'])
        else:
            config['selection_add'] = 0
        if 'fitness' in tmp:
            config['fitness'] = float(tmp['fitness'])
        else:
            config['fitness'] = 0.5
    else:
        print("Configuration fail. See example.")
        exit(1)
    return config


if __name__ == '__main__':
    solve()
