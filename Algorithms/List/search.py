def binary_search(needle, haystack):
    """ Binary search is a technique for locating a target item in a sorted list by repeatedly
    determining which half of the list the item is in. The most impartial way to search is to start with
    the middle item, and then ascertain if the item you’re searching for is greater or lesser. """
    def aux(start_cursor, end_cursor):
        if start_cursor > end_cursor:
            return None
        mid = (start_cursor + end_cursor) // 2
        if needle == haystack[mid]:
            return mid
        return aux(mid + 1 if needle > haystack[mid] else start_cursor,
                   mid - 1 if needle < haystack[mid] else end_cursor)
    return aux(0, len(haystack) - 1)

print(binary_search("Y", "AEIOPRTUYZ"))
