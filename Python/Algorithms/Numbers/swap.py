
if __name__ == '__main__':
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
