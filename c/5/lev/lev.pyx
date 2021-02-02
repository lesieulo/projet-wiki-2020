import time
import numpy
cimport numpy

def f():
    cdef unsigned long long int maxval
    cdef unsigned long long int total
    cdef int k
    cdef double t1, t2, t
    cdef numpy.ndarray arr

    maxval = 10000
    arr = numpy.arange(maxval)

    for k in arr:
        total = total + k
    print("Total =", total)

def g(int n):
    a = numpy.ones((n, n))
    a[2, 2] = 3
    return a
    
def g2(int n):
    a = numpy.empty((n, n), dtype=str)
    a[2, 2] = 'f'
    return a

def h(str s, str t):
    cdef int m = len(s)
    cdef int n = len(t)
    cdef np.ndarray a = numpy.empty((m, n), dtype=str)
    a[1, 1] = s[0]
    print("taille", m, n)
    return a




