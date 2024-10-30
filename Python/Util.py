import inspect
import re
from datetime import timedelta, datetime
from struct import pack, unpack
from typing import Iterable, Sized, Callable

import numpy as np
# import nbmerge
import pandas as pd
import pytz
from keras.datasets import mnist

training_set, test_set = mnist.load_data()
train_images, train_labels = training_set
test_images, test_labels = test_set
# Si le debug de PyCharm bug, check les __repr__"

""" Lists """


def rotate(lst, n=1):
    return lst[-n:] + lst[:-n]


def str_to_ord(text: str):
    return [ord(character) for character in text]


def contain_all(base: Iterable and Sized, elements: set):
    return all((element in base for element in elements))


def gen_list_around_value(value, length):
    start = value - (length // 2) * (value / length)
    if length % 2 == 0:
        start += (value / length) / 2
    return [start + i * (value / length) for i in range(length)]

""" Logical Operators """


def xor(a, b):
    return (a and not b) or (not a and b)


""" Bitwise Operators """


def get_bit(value, index):
    """put to 0 all bits except for the one at the position index
    >>> bin(get_bit(0b10000000, index=5))
    '0b0'
    >>> bin(get_bit(0b10100000, index=5))
    '0b100000'
    """
    return value & (1 << index)


def get_normalized_bit(value, bit_index):
    """output the bit in the 5th position
    >>> get_normalized_bit(0b10000000, bit_index=5)
    0
    >>> get_normalized_bit(0b10100000, bit_index=5)
    1
    """
    return (value >> bit_index) & 1


def set_bit(value, bit_index):
    """Retains all the original bits while enforcing a binary one at the specified index.
    >>> bin(set_bit(0b10000000, bit_index=5))
    '0b10100000'
    """
    return value | (1 << bit_index)


def clear_bit(value, bit_index):
    """copy all binary digits while enforcing zero at one specific index.
    & operator evaluates two_complement_representation representation on both operands
    """
    return value & ~(1 << bit_index)


def two_complement_representation(x: int):
    mask = 2 ** (8 * ((x.bit_length() // 8) + 1)) - 1
    return x & mask


def two_complement_representation_2(x: int):
    shift = 8 * ((x.bit_length() // 8) + 1)
    return x % (1 << shift)


def two_complement_representation_3(x: int):
    from ctypes import c_uint8 as unsigned_byte
    return unsigned_byte(x).value


""" Float """


def float_to_bin(x):
    """IEEE 754 standard"""
    return "".join([f"{b:08b}" for b in pack(">d", x)])


def bin_to_float(bits):
    """IEEE 754 standard"""
    return unpack(">d", bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)))[0]


""" Files """


def merge_files(filenames: list[str], dest: str = "main.py", end="\n"):
    with open(dest, 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                files_txt = infile.read()
                outfile.write(files_txt)
            outfile.write(end)


# def merge_ipynb_files(filenames: list[str], dest: str = "dest.ipynb"):
#     nbmerge.write_notebook(nbmerge.merge_notebooks(dest, filenames, verbose=True), dest)


""" Times """


def now(utc=False, offset_h=0, offset_m=0, offset_s=0) -> datetime:
    offset = timedelta(hours=offset_h, minutes=offset_m, seconds=offset_s)
    return offset + (datetime.utcnow() if utc else datetime.now())


def to_datetime(obj, pattern: str = "%Y/%m/%d %H:%M:%S") -> datetime:
    if type(obj) is datetime:
        return obj
    try:
        return datetime.fromtimestamp(int(obj))
    except (ValueError, AttributeError, TypeError):
        default_value = pattern == "%Y/%m/%d %H:%M:%S"
        str_obj = str(obj).replace("-", "/") if default_value else str(obj)
        return datetime.strptime(str_obj, pattern)


def to_timestamp(obj, pattern: str = "%Y/%m/%d %H:%M:%S") -> float:
    if type(obj) in (float, int):
        return obj
    try:
        return obj.timestamp()
    except (ValueError, AttributeError, TypeError):
        return to_timestamp(to_datetime(obj, pattern=pattern))


def elapsed_timedelta(date_time: datetime):
    return datetime.now() - date_time


def elapsed_seconds(date_time: datetime):
    return (datetime.now() - date_time).total_seconds()


def elapsed_minutes(date_time: datetime):
    return elapsed_seconds(date_time) / 60


def generate_datetime(start: datetime, end: datetime, freq="T") -> list[str]:
    return sorted(map(str, pd.date_range(start=start, end=end, freq=freq).to_pydatetime().tolist()))


def timeit_trivial(fun: Callable, *args, n=100):
    start = now()
    for _ in range(n):
        fun(*args)
    execution_time = round(elapsed_seconds(start) / n * 1000, 3)
    print(fun.__name__, execution_time, "ms")
    return execution_time


def timeit(fun: Callable, *args) -> float:
    """ Estimate an execution time of a function as milliseconds
    Repeat at least 10 times the function to memoize it into the cache then
    |Repeat at least 1 time the function to refresh it into the cache
    |Estimate the execution time with at least 10 executions, this is regrouped as one execution time by calculating its average
    |Repeat that 5 times
    Calculate the average of estimated executions times
    Return the average of estimated executions times as milliseconds
    """
    repeat_call_min = 10
    sec_elapsed_minimal = 1
    total_repeat = 5
    times_estimate = []
    start = now()
    i = 0
    while elapsed_seconds(start) < sec_elapsed_minimal or i < repeat_call_min:
        # "charging in cache"
        fun() if len(args) == 0 else fun(*args)
        i += 1
        if elapsed_seconds(start) <= sec_elapsed_minimal:
            repeat_call_min += 1
    for _ in range(total_repeat):
        for _ in range(int(repeat_call_min / 10)):
            fun() if len(args) == 0 else fun(*args)
        start = now()
        for _ in range(repeat_call_min):
            fun() if len(args) == 0 else fun(*args)
        times_estimate.append(elapsed_seconds(start) / repeat_call_min)
    execution_time = round(sum(times_estimate) / len(times_estimate) * 1000, 6)
    print(fun.__name__, execution_time, "ms", len(times_estimate) * repeat_call_min, "called")
    return execution_time


def search_tz(city: str) -> pytz:
    """ Cherche une ville dans pytz.all_timezones et retourne sa timezone. """
    return pytz.timezone(list(name for name in pytz.all_timezones if city.capitalize() in name)[0])


""" Regex """

re_decimal = re.compile(r"([0-9]+)\.([0-9]+)")
re_int = re.compile(r"([-+]?[0-9]+([eE][-+]?[0-9]+)?)")
re_float = re.compile(r"([-+]?[0-9,]*\.?[0-9,]+([eE][-+]?[0-9,]+)?)")
re_time_hms = re.compile(r"((([0-9]?[0-9]) *h *)?(([0-9]?[0-9]) *m *)?(([0-9]?[0-9]) *s *)?)")
re_time_dot = re.compile(r"((([0-9]?[0-9]) *: *)?(([0-9]?[0-9]) *: *)([0-9]?[0-9]))")
re_alphanum_char = re.compile(r"([a-zA-Z0-9]+)")
re_num_char = re.compile(r"([0-9]+)")
re_alpha_char = re.compile(r"([a-zA-Z]+)")
re_html_blaze = re.compile(r"(<.*?>)")

""" print """

def pr(*args):
    list(map(print, args))

""" Introspection """


def print_code_function(fun: Callable):
    print("\n".join(inspect.getsource(fun).split("\n")))


if __name__ == '__main__':
    print(bin(clear_bit(0xff, 5)))
    # print(bin(a & b))
