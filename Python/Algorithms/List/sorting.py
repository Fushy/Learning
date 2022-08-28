def quick_sort(lst):
    if len(lst) == 0:
        return []
    return quick_sort([x for x in lst[1:] if x <= lst[0]]) + [lst[0]] + quick_sort([x for x in lst[1:] if x > lst[0]])


if __name__ == '__main__':
    print(quick_sort([5, 8, 9, 6, 7, 4, 5, 8, 9, 6, 3, 0]))
