import random
import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp

from cpython cimport array
from libc.stdlib cimport rand, RAND_MAX
from collections import deque
import time
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free


@cython.boundscheck(False)
@cython.cdivision(True)
def sa(inst, soll, temperature, cooling_coef, min_temp, inner_loop):

    cdef int n
    cdef int max_weight
    cdef float sol = float(soll)
    n = int(inst[1])
    max_weight = int(inst[2])

    cdef np.ndarray[np.int64_t, ndim=1] prices = np.array(inst[3:][1::2], dtype=np.int64)
    cdef np.ndarray[np.int64_t, ndim=1] weights = np.array(inst[3:][::2], dtype=np.int64)

    cdef list values = []


    cdef int best = 0
    cdef np.ndarray[np.int64_t, ndim=1] bestS = np.zeros(n, dtype=np.int64)

    cdef int current = 0
    cdef np.ndarray[np.int64_t, ndim=1] currentS = np.zeros(n, dtype=np.int64)

    cdef np.ndarray[np.int64_t, ndim=1] workS = np.zeros(n, dtype=np.int64)

    cdef float temp = temperature
    cdef float cool_coef = cooling_coef
    cdef float minT = min_temp
    cdef int loop = inner_loop
    cdef int i, bit, scoreN, weightN

    while (temp > minT):
        
        values.append([temp, best, current, (sol-best)/sol, (sol-current)/sol])

        for i in range(loop):

            # random flip
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
    
    return (best, bestS, (sol-best)/sol, values)

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
