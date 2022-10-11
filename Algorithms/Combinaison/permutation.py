def permutations(word: str, duplicate=True) -> list[str]:  # O(n * n!)
    """ All specific ordering of all elements from E. """
    if len(word) <= 1:
        return list(word) if duplicate else set(word)
    reductions = permutations(word[1:])
    perms = [] if duplicate else set()
    for reduction in reductions:
        for i in range(len(reduction) + 1):
            value = reduction[:i] + word[0] + reduction[i:]
            perms.append(value) if duplicate else perms.add(value)
    return perms


if __name__ == '__main__':
    print("{} {}".format("permutation", "nan"), permutations("nan"))
    print("{} {}".format("permutation", "nan"), permutations("nan", duplicate=False))
    # print("{} {}".format("permutation", "Nan").ljust(spaces), permutation_sans_doublons("Nan"))
