def permutations(word: str, duplicate=True) -> list[str]:
    if len(word) <= 1:
        return list(word) if duplicate else set(word)
    reductions = permutations(word[1:])
    return_values = [] if duplicate else set()
    for reduction in reductions:
        for pos in range(len(reduction) + 1):
            value = reduction[:pos] + word[0] + reduction[pos:]
            return_values.append(value) if duplicate else return_values.add(value)
    return return_values


if __name__ == '__main__':
    print("{} {}".format("permutation", "nan"), permutations("nan"))
    print("{} {}".format("permutation", "nan"), permutations("nan", duplicate=False))
    # print("{} {}".format("permutation", "Nan").ljust(spaces), permutation_sans_doublons("Nan"))
