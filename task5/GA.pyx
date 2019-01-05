import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp
from libc.stdlib cimport rand, RAND_MAX
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

@cython.boundscheck(False)
@cython.cdivision(True)
def ga(n_var, n_clause, weights, clause, gen_count, gen_size, mut, cross, elitism, t_size):

    cdef int i, j, gen, _n_var, _n_clause, _gen_count, _gen_size, _elitism, _best_score = 0, _total_weight = 0, _t_size
    cdef double _mut, _cross
    cdef int _good_clause, _weight, _sum_solutions
    if elitism is True:
        _elitism = 1
    else:
        _elitism = 0
    _n_clause = n_clause
    _n_var = n_var
    _gen_count = gen_count
    _gen_size = gen_size
    _mut = mut
    _cross = cross
    _t_size = t_size

    # For ast access
    cdef np.ndarray[np.int64_t, ndim=1] _weights = np.array(weights, dtype=np.int64)
    # Data for plots
    cdef np.ndarray[np.int64_t, ndim=1] n_sol = np.zeros(_gen_count, dtype=np.int64)
    cdef np.ndarray[np.int64_t, ndim=2] n_clau = np.zeros((_gen_count, _gen_size), dtype=np.int64)
    cdef np.ndarray[np.float64_t, ndim=2] generations = np.zeros((_gen_count, _gen_size), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=1] _population_fitness = np.zeros(_gen_size, dtype=np.float64)
    # Clause and population
    cdef int ** _clauses = load_clause(clause, _n_clause)
    cdef int ** _population = <int **> PyMem_Malloc(_gen_size * sizeof(int*))
    # Copy for create new generation using selection, but do selection on original population
    cdef int ** _population_tmp = <int **> PyMem_Malloc(_gen_size * sizeof(int*))
    cdef int pos = 0, maximum_fitness_index = -1, parent_2_index, parent_1_index
    cdef int ** _population_switch
    cdef int * _child_1  = <int *> PyMem_Malloc(_n_var * sizeof(int))
    cdef int * _child_2 = <int *> PyMem_Malloc(_n_var * sizeof(int))
    cdef int * _best = <int *> PyMem_Malloc(_n_var * sizeof(int))

    # Generate random population
    for i in range(_gen_size):
        _population[i] = random_fen(_n_var)
        _population_tmp[i] = random_fen(_n_var)

    # Count total weight
    for i in range(_n_var):
        _total_weight += _weights[i]

    # Main generation cycle
    for gen in range(_gen_count):

        _sum_solutions = 0
        for i in range(_gen_size):

            # do stats to print
            _good_clause = satisfied_clauses(_clauses, _n_clause, _population[i])
            _weight = solution_weight(_population[i], _n_var, _weights)
            if _good_clause == _n_clause:
                _sum_solutions += 1
            # compute fitness
            _population_fitness[i] = fitness(0.8, _good_clause, _n_clause, _weight, _total_weight)

            # stats
            generations[gen, i] = _population_fitness[i]
            n_clau[gen, i] = _good_clause

            # save the best
            if _population_fitness[i] > _best_score:
                copy_sol(_n_var, _best, _population[i])

        # stats for number of proper solution in population
        n_sol[gen] = _sum_solutions

        if _elitism == 1:
            maximum_fitness_index = 0
            # find the best
            for i in range(_gen_size):
                if _population_fitness[i] > maximum_fitness_index:
                    maximum_fitness_index = i
            # copy to new solution
            copy_sol(_n_var, _population_tmp[pos], _population[maximum_fitness_index])

        while pos < _gen_size:

            # do selection select a and b
            parent_1_index = selection(_population, _gen_size, _n_var, _population_fitness, _t_size)
            parent_2_index = selection(_population, _gen_size, _n_var, _population_fitness, _t_size)

            # cross parent if need
            if rand()/<float>RAND_MAX < _cross:
                # TODO:do cross if need
                uniform_crossover(_population[parent_1_index], _population[parent_2_index], _child_1, _child_2, _n_var)
                copy_sol(_n_var, _population_tmp[pos], _child_1)
                pos += 1
                if pos >= _gen_size:
                    break
                copy_sol(_n_var, _population_tmp[pos], _child_1)
                pos += 1
            else:
                copy_sol(_n_var, _population_tmp[pos], _population[parent_1_index])
                pos += 1
                if pos >= _gen_size:
                    break
                copy_sol(_n_var, _population_tmp[pos], _population[parent_2_index])
                pos += 1

            # TODO:save to population two of them


        pos = 0

        # do mutation
        for i in range(_gen_size):
            mutation(_population_tmp[i], _n_var, _mut)

        # switch population
        _population_switch = _population_tmp
        _population_tmp = _population
        _population = _population_switch


    free_mem(_clauses, _n_clause)
    free_mem(_population, _gen_size)
    free_mem(_population_tmp, _gen_size)
    PyMem_Free(_child_1)
    PyMem_Free(_child_2)
    PyMem_Free(_best)
    return _best_score, generations, n_sol, n_clau

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void uniform_crossover(int * parent_1, int * parent_2, int * child_1, int * child_2, int size):
    cdef int i
    for i in range(size):
        if rand()/<float>RAND_MAX < 0.5:
            child_1[i] = parent_1[i]
            child_2[i] = parent_2[i]
        else:
            child_1[i] = parent_2[i]
            child_2[i] = parent_1[i]
    return

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void two_point_crossover(int * parent_1, int * parent_2, int * child_1, int * child_2, int size):
    cdef int first, second, i = 0
    while True:
        ...
    return

@cython.boundscheck(False)
@cython.cdivision(True)
cdef int selection(int ** _population, int size, int n_var, np.float64_t[:] fitness, int _t_size):
    cdef int maximum_index = -1, i, random_index
    cdef double maximum_value = -1
    for i in range(_t_size):
        random_index = rand() % size
        if fitness[random_index] > maximum_value:
            maximum_value = fitness[random_index]
            maximum_index = random_index
    return maximum_index


@cython.boundscheck(False)
@cython.cdivision(True)
cdef void mutation(int * one, int size, double mut):
    cdef int i
    for i in range(size):
        if rand()/<float>RAND_MAX < mut:
            if one[i] == 1:
                one[i] = 0
            else:
                one[i] = 1


@cython.boundscheck(False)
cdef int solution_weight(int * one, int size, np.int64_t[:] weights):
    cdef int score = 0, i
    for i in range(size):
        score += one[i] * weights [i]
    return score


@cython.boundscheck(False)
@cython.cdivision(True)
@cython.wraparound(False)
cdef int satisfied_clauses(int ** clauses, int n_clauses, int * variables):
    cdef int cnt, i, j
    cnt = 0
    for i in range(n_clauses):
        for j in range(clauses[i][0]):
            if clauses[i][j+1] < 0 and variables[abs(clauses[i][j+1])-1] == 0:
                cnt += 1
                break
            if clauses[i][j+1] > 0 and variables[abs(clauses[i][j+1])-1] == 1:
                cnt += 1
                break
    return cnt


@cython.boundscheck(False)
@cython.cdivision(True)
cdef void copy_sol(int size, int * first, int * second):
    cdef int i
    for i in range(size):
        first[i] = second[i]


@cython.boundscheck(False)
@cython.cdivision(True)
cdef double fitness(double per_for_good, int good_clause, int n_clause, int weight, int total_weight):
    return per_for_good * (<double> good_clause / n_clause) + (1-per_for_good) * (<double> weight / total_weight)


@cython.boundscheck(False)
cdef int * random_fen(int size):
    cdef int * tmp = <int *> PyMem_Malloc(size*sizeof(int))
    for i in range(size):
        tmp[i] = rand() % 2
    return tmp


@cython.boundscheck(False)
cdef int** load_clause(clause, int n_clauses):

    cdef int tmp, i, j, temp
    cdef int ** clauses = <int **> PyMem_Malloc(n_clauses*sizeof(int*))

    for i in range(n_clauses):
        tmp = len(clause[i])
        clauses[i] = <int *> PyMem_Malloc((tmp+1)*sizeof(int))
        clauses[i][0] = tmp
        for j in range(tmp):
            clauses[i][j+1] = int(clause[i][j])

    return clauses


@cython.boundscheck(False)
cdef void free_mem(int ** array, int length):
    for i in range(length):
        PyMem_Free(array[i])
    PyMem_Free(array)
