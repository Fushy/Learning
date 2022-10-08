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

def ackermann(m, n):
    if m <= 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    elif n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))


def is_even(n: int):
    return n % 2 == 0


def is_odd(n: int):
    return n % 2 != 0

def get_decimal(x: float):
    return x % 1

def roundup(x: float):
    return int(x) if get_decimal(x) == 0 else int(x) + 1

def pow_rec(a: float, n: int):
    if n == 1:
        return a
    elif n % 2 == 0:
        result = pow_rec(a, n // 2)
        return result * result
    elif n % 2 == 1:
        result = pow_rec(a, n // 2)
        return result * result * a


if __name__ == '__main__':
    fibonacci_rec(100)
    print(timeit(factorial_lib, 100))
    print(timeit(factorial_iter, 100))
    print(timeit(factorial_fun, 100))
    print(timeit(factorial_rec, 100))
