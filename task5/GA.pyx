import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp
from libc.stdlib cimport rand, RAND_MAX
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free


@cython.boundscheck(False)
@cython.cdivision(True)
def ga(n_var, n_clause, weights, clause, gen_count, gen_size, mut, cross, elitism, t_size):

    cdef int i, j, k, _n_var, _n_clause, _gen_count, _gen_size, _elitism, best_score
    cdef double _mut, _cross, _t_size

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

    # Data for plots
    cdef np.ndarray[np.int64_t, ndim=1] n_sol = np.zeros(_gen_count, dtype=np.int64)
    cdef np.ndarray[np.int64_t, ndim=1] n_clau = np.zeros(_gen_count, dtype=np.int64)
    cdef np.ndarray[np.int64_t, ndim=1] n_best_score = np.zeros(_gen_count, dtype=np.int64)
    cdef np.ndarray[np.int64_t, ndim=2] generations = np.zeros((_gen_count, _gen_size), dtype=np.int64)

    # Clause and population
    cdef int ** clauses = <int **> PyMem_Malloc(_n_clause * sizeof(int*))
    cdef int ** populations = <int **> PyMem_Malloc(_gen_size * sizeof(int*))






    return best_score, generations, n_sol, n_clau, n_best_score

"""
    
            bit = rand() % n
            if workS[bit] == 0:
                workS[bit] = 1
            else:
                workS[bit] = 0

            # score and weight -> when is too heavy continue
            scoreN = score(n, workS, prices)
            weightN = weight(n, workS, weights)
            if weightN > max_weight: 
                continue

            # if better, get it and continue
            if scoreN > current:
                copy_sol(n, currentS, workS)
                current = scoreN
                if scoreN > best:
                    copy_sol(n, bestS, workS)
                    best = scoreN
                continue

            # if is worse I get it with probability based on temperature
            if (rand()/<float>RAND_MAX) < exp(-(current - scoreN)/temp):
                copy_sol(n, currentS, workS)
                current = scoreN
                continue

            copy_sol(n, workS, currentS)
            
        temp = cool_coef * temp
    
    return (best, bestS, (sol-best)/sol, values)"""

@cython.boundscheck(False)
@cython.cdivision(True)
cdef int score(int len, np.int64_t[:] ins, np.int64_t[:] prices):
    cdef int score = 0
    cdef int i
    for i in range(len):
        if ins[i] == 1:
            score += prices[i]
    return score


@cython.boundscheck(False)
@cython.cdivision(True)
cdef int weight(int len, np.int64_t[:] ins, np.int64_t[:] weights):
    cdef int weight = 0
    cdef int i
    for i in range(len):
        if ins[i] == 1:
            weight += weights[i]
    return weight

@cython.boundscheck(False)
@cython.cdivision(True)
cdef void copy_sol(int len, np.int64_t[:] first, np.int64_t[:] second):
    cdef int i
    for i in range(len):
        first[i] = second[i]
