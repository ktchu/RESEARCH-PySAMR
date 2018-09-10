from numba import jit
from numpy import arange
import timeit

# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]

    return result


def sum2d_no_numba(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]

    return result

# force compilation when module is imported
b = arange(9).reshape(3,3)
sum2d(b)

a = arange(1000000).reshape(1000, 1000)

if __name__ == '__main__':
    print(timeit.timeit('sum2d(a)', number=1000,
                        setup="from __main__ import sum2d, a"))
    print(timeit.timeit('sum2d_no_numba(a)', number=100,
                        setup="from __main__ import sum2d_no_numba, a"))
#print(sum2d(a))
