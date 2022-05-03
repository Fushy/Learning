"""String"""
from struct import pack, unpack


def str_to_ord(text: str):
    return [ord(character) for character in text]


"""Logical Operators"""


def xor(a, b):
    return (a and not b) or (not a and b)


"""Bitwise Operators"""


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


"""Float"""


def float_to_bin(x):
    """IEEE 754 standard"""
    return "".join([f"{b:08b}" for b in pack(">d", x)])


def bin_to_float(bits):
    """IEEE 754 standard"""
    return unpack(">d", bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)))[0]


"""Files"""


def merge_files(filenames: list[str], dest: str = "main.py"):
    with open(dest, 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                outfile.write(infile.read())
            outfile.write("\n")


if __name__ == '__main__':
    print(bin(clear_bit(0xff, 5)))
    # print(bin(a & b))
