import math
from functools import reduce

from Util import timeit


def swap_algorithms():
    # swap algorithm with Python syntax
    a, b = 1, 2
    b, a = a, b
    print(a, b)

    # swap algorithm with xor
    a, b = 3, 4
    a ^= b
    b ^= a
    a ^= b
    print(a, b)

    # swap algorithm with add & sub
    a, b = 5, 6
    a += b
    b = a - b
    a -= b
    print(a, b)


def factorial_iter(n):
    result = 1
    for n in range(2, n + 1):
        result *= n
    return result


def factorial_rec(n):
    if n in [0, 1]:
        return 1
    return n * factorial_rec(n - 1)


def factorial_fun(n):
    return reduce(lambda x, y: x * y, range(1, n + 1) or [1])


def factorial_lib(n):
    return math.factorial(n)


def fibonacci_rec(n):
    if n in (0, 1):
        return n
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == '__main__':
    fibonacci_rec(100)
    print(timeit(factorial_lib, 100))
    print(timeit(factorial_iter, 100))
    print(timeit(factorial_fun, 100))
    print(timeit(factorial_rec, 100))
