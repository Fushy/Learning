def reverse_1(lst):
    if len(lst) <= 1:
        return lst
    return reverse_1(lst[1:]) + lst[0]


def reverse_2(lst):
    if len(lst) <= 1:
        return lst
    return lst[-1] + reverse_2(lst[:-1])


if __name__ == '__main__':
    print(reverse_1('abcde'))
    print(reverse_2('abcde'))
