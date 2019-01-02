import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp
from libc.stdlib cimport rand, RAND_MAX
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

@cython.boundscheck(False)
@cython.cdivision(True)
def ga(n_var, n_clause, weights, clause, gen_count, gen_size, mut, cross, elitism, t_size):

    cdef int i, j, gen, _n_var, _n_clause, _gen_count, _gen_size, _elitism, _best_score = 0, _total_weight = 0
    cdef float _mut, _cross, _t_size
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
    cdef int * _a = <int *> PyMem_Malloc(_n_var * sizeof(int))
    cdef int * _b = <int *> PyMem_Malloc(_n_var * sizeof(int))
    cdef int * _best = <int *> PyMem_Malloc(_n_var * sizeof(int))

    # Generate random population
    for i in range(_gen_size):
        _population[i] = random_fen(_n_var)

    # Count total weight
    for i in range(_n_var):
        _total_weight += _weights[i]

    # Main generation cycle
    for gen in range(_gen_count):

        _sum_solutions = 0
        for i in range(_gen_size):

            _good_clause = satisfied_clauses(_clauses, _n_clause, _population[i])
            _weight = solution_weight(_population[i], _n_var, _weights)
            if _good_clause == _n_clause:
                _sum_solutions += 1
            _population_fitness[i] = fitness(0.95, _good_clause, _n_clause, _weight, _total_weight)

            generations[gen, i] = _population_fitness[i]
            n_clau[gen, i] = _good_clause

            if _population_fitness[i] > _best_score:
                copy_sol(_n_var, _best, _population[i])

        n_sol[gen] = _sum_solutions

        if rand()/<float>RAND_MAX < _cross:
                ind = rand() % n_var

        for i in range(_gen_size):
            mutation(_population[i], _n_var, _mut)

        # dokud nenagradim populaci opakuju
            # selektnu jedince
            # pokud vyjde krizeni krizim
            # Pote mutace
            # Podle counteru copiruji do reseni

    free_mem(_clauses, _n_clause)
    free_mem(_population, _gen_size)
    PyMem_Free(_a)
    PyMem_Free(_b)
    PyMem_Free(_best)
    return _best_score, generations, n_sol, n_clau

@cython.boundscheck(False)
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
