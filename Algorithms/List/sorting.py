import statistics


def quicksort_trivial(lst):
    if len(lst) <= 1:
        return lst
    pivot = statistics.median([lst[0], lst[len(lst) // 2], lst[-1]])
    items_less = [n for n in lst if n < pivot]
    pivot_items = [n for n in lst if n == pivot]
    items_greater = [n for n in lst if n > pivot]
    return quicksort_trivial(items_less) + pivot_items + quicksort_trivial(items_greater)


def quick_sort(lst):
    if len(lst) <= 1:
        return lst
    return quick_sort([x for x in lst[1:] if x <= lst[0]]) + [lst[0]] + quick_sort([x for x in lst[1:] if x > lst[0]])


if __name__ == '__main__':
    print(quicksort_trivial([5, 8, 9, 6, 7, 4, 5, 8, 9, 6, 3, 0]))
    print(quick_sort([5, 8, 9, 6, 7, 4, 5, 8, 9, 6, 3, 0]))
