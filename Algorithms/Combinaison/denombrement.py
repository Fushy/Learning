# https://mathematice.fr/fichiers/bts/denombrement.pdf

import itertools
import math
from typing import Iterable, Callable, Sized, Any, TypeVar

A = TypeVar("A")
B = TypeVar("B")


# Pas d'utilisations de set pour les ensembles afin d'obtenir un ensemble trie

def cardinal_produit_cartesien(n: int, k: int) -> int:
    return n * k


def produit_cartesien(E: A, F: B) -> list[tuple[A, B]]:
    return sorted(itertools.product(E, F))


def cardinal_p_uplets(n: int, p: int) -> int:
    return n ** p


def p_uplets(E, p=None) -> list[tuple]:
    if p is None:
        return p_uplets(E, len(E))
    elif p == 0:
        return [()]
    return sorted([(e,) + p_uplet
                   for e in E
                   for p_uplet in p_uplets(E, p - 1)])


def cardinal_applications_E_dans_F(cardinal_E: int, cardinal_F: int) -> int:
    return cardinal_F ** cardinal_E


def applications_E_dans_F(E: A, F: B = None) -> list[tuple[B, ...]]:  # notation mathematique Map(E; F)
    """ Ensemble d'applications differentes d'un ensemble fini E dans un ensemble fini F.
        E l'ensemble de depart et F est l'ensemble d'arrive donc F est repete E fois. """
    E = sorted(E)
    if F is None:
        F = list(E)
    F = sorted(F)
    return sorted([tuple(uplet[i] for i in range(len(E)))
                   for uplet in p_uplets(F, len(E))])
    # return sorted([[(E[i], uplet[i]) for i in range(len(E))] for uplet in p_uplets(F, len(E))])


def cardinal_permutation(n: int) -> int:
    return math.factorial(n)


def permutations(E, n=None, join_str=False, duplicate=True):
    """ Un arrangement de n elements.
        On tire successivement et sans remise dans un ensemble E de n elements, n elements. """
    if n is None:
        n = len(E)
    if join_str:
        permutations = map(lambda x: "".join(x).capitalize(), itertools.permutations(E, n))
        return sorted(permutations) if duplicate else sorted(set(permutations))
    return sorted(itertools.permutations(E, n)) if duplicate else sorted(set(itertools.permutations(E, n)))


def permutations_all_size(elements):
    return [set(permutations(elements, n=i)) for i in range(len(elements))]


def cardinal_arrangement(n: int, k: int) -> int:
    return math.factorial(n) // math.factorial(n - k)


def arrangement(E, k):
    """ Ensemble d'arrangement de k elements parmi un ensemble E de n elements.
        On tire successivement et sans remise k elements dans un ensemble E de n elements.
        Ensemble d'injections de k elements parmi un ensemble E de n elements. """
    return sorted(itertools.permutations(E, k))


def cardinal_combinaison(n: int, k: int) -> int:
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def combinaison(E, k):
    """ Combinaison de k elements choisis parmi E.
        Dans un ensemble E de n elements, on tire simultanement k elements.
        Ensemble de sous-ensemble de cardinal k d'un ensemble E. """
    # return sorted([tuple(sorted(partie)) for partie in itertools.combinations(E, k)])
    return [partie for partie in sous_ensembles_differents(E) if len(partie) == k]


def combinaison_sans_repetition(E, k):
    return sorted(set(combinaison(E, k)))


def cardinal_sous_ensembles_differents(cardinal: int) -> int:
    return 2 ** cardinal


def sous_ensembles_differents(E) -> list[tuple]:
    """ Ensemble de sous ensemble (ou de parties) differents d'un ensemble fini E. """
    return sorted(itertools.chain.from_iterable(
        [tuple(sorted(combination)) for combination in itertools.combinations(E, i)]
        for i in range(len(E) + 1)),
        key=lambda x: (len(x), *x))


def cardinal_correspondances(cardinal_E: int, cardinal_F: int) -> int:
    return 2 ** (cardinal_E * cardinal_F)


def correspondances(E, F):
    """ Ensemble de correspondances differente de deux ensembles fini E et F """
    return sous_ensembles_differents(produit_cartesien(E, F))


def rotate(E, n=1) -> tuple[Any]:
    return tuple(E[-n:] + E[:-n])


def rotates(E: Iterable and Sized) -> list[Any]:
    return [r for r in (rotate(E, i) for i in range(len(E)))]


def classes_equivalences(E: Iterable, relation: Callable[[Iterable and Sized], list] = rotates) -> list:
    """ Regroupe toutes les classes d'equivalence sous forme d'une liste grâce à la relation :relation:.
    >>> classes_equivalences(["123", "231", "132"])
    [(('1', '2', '3'), ('3', '1', '2'), ('2', '3', '1')),
    (('1', '3', '2'), ('2', '1', '3'), ('3', '2', '1')),
    (('2', '3', '1'), ('1', '2', '3'), ('3', '1', '2'))]
    """
    classe_equivalence = {}.fromkeys(tuple(classe) for classe in map(relation, E))
    return sorted(classe_equivalence, key=lambda x: (len(x), x))


def first_element_of_each_equivalences_classes(E, relation=rotates):
    return sorted(classes[0] for classes in classes_equivalences(E, relation))


if __name__ == '__main__':
    spaces = 70
    E = 1, 2
    # F = "A", "B", "C"
    F = "LEFT", "RIGHT", "UP", "BOT"
    x = len(E)
    y = len(F)

    print("{} {}".format("rotates", E).ljust(spaces), rotates(E))
    print("{} {}".format("rotates", F).ljust(spaces), rotates(F))

    print("{} {} {}".format("produit_cartesien", E, F).ljust(spaces), produit_cartesien(E, F))
    print("{} {} {}".format("produit_cartesien", F, E).ljust(spaces), produit_cartesien(F, E))

    print("{} {}".format("p_uplets", E).ljust(spaces), p_uplets(E))
    print("{} {}".format("p_uplets", F).ljust(spaces), p_uplets(F))
    print("{} {} {}".format("p_uplets", F, 2).ljust(spaces), p_uplets(F, 2))

    print("{} {}".format("applications_E_dans_F", E).ljust(spaces), applications_E_dans_F(E))
    print("{} {} {}".format("applications_E_dans_F", E, F).ljust(spaces), applications_E_dans_F(E, F))
    print("{} {} {}".format("applications_E_dans_F", F, E).ljust(spaces), applications_E_dans_F(F, E))

    print("{} {}".format("permutation", E).ljust(spaces), permutations(E))
    print("{} {}".format("permutation", F).ljust(spaces), permutations(F))
    print("{} {}".format("permutations_all_size", F).ljust(spaces), permutations_all_size(F))
    print("{} {} {}".format("permutation", "Nan", "join_str=True").ljust(spaces), permutations("Nan", join_str=True))
    print("{} {} {}".format("permutation", "Nan", "join_str=True, duplicate=False").ljust(spaces),
          permutations("Nan", join_str=True, duplicate=False))

    print("{} {} {}".format("arrangement", F, 1).ljust(spaces), arrangement(F, 1))
    print("{} {} {}".format("arrangement", F, 2).ljust(spaces), arrangement(F, 2))
    print("{} {} {}".format("arrangement", F, 3).ljust(spaces), arrangement(F, 3))
    print("{} {} {}".format("arrangement", F, 4).ljust(spaces), arrangement(F, 4))

    print("{} {} {}".format("combinaison", F, 1).ljust(spaces), combinaison(F, 1))
    print("{} {} {}".format("combinaison", F, 2).ljust(spaces), combinaison(F, 2))
    print("{} {} {}".format("combinaison", F, 3).ljust(spaces), combinaison(F, 3))
    print("{} {} {}".format("combinaison", F, 4).ljust(spaces), combinaison(F, 4))

    print("{} {}".format("sous_ensembles_differents", E).ljust(spaces), sous_ensembles_differents(E))
    print("{} {}".format("sous_ensembles_differents", F).ljust(spaces), sous_ensembles_differents(F))

    print("{} {} {}".format("correspondances", E, F).ljust(spaces), correspondances(E, F))
    print("{} {} {}".format("correspondances", F, E).ljust(spaces), correspondances(F, E))

    print("{} {}".format("classes_equivalences", F).ljust(spaces), classes_equivalences(F))
    print("{} {}".format("first_element_of_each_classes_equivalences", F).ljust(spaces),
          first_element_of_each_equivalences_classes(F))
