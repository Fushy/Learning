#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe à l'aide d'une matrice d'adjacence. Les n sommets
sont identifiés par de simples naturels (0, 1, 2, ..., n-1)."""


def checkType(*args):
    from inspect import stack
    i = 0
    while i < len(args):
        if type(args[i]) != args[i + 1]:
            string = "\nLe type de l'argument numéro " + str(i + 1) + " de la méthode " + str(
                stack()[2][3]) + " n'est pas correct : \n\t" + repr(args[i]) + " -> " + str(args[i + 1])
            raise NameError(string)
        i += 2


class MatriceAdjacence(object):
    def __init__(self, num=0):
        """Initialise un graphe sans arêtes sur num sommets.

        >>> G = MatriceAdjacence()
        >>> G._matrice_adjacence
        []
        """
        self._matrice_adjacence = [[0] * num for _ in range(num)]

    def affiche_matrice(self, vide=False, arete=False):
        print("\t", end="")
        for i in range(len(self._matrice_adjacence)):
            print(i, end="\t")
        print()
        for i in range(len(self._matrice_adjacence)):
            print(i, "\t", end="")
            for j in range(len(self._matrice_adjacence)):
                if vide:
                    if self._matrice_adjacence[i][j] == 0:
                        print(" \t", end="")
                    else:
                        print(self._matrice_adjacence[i][j], "\t", end="")
                else:
                    print(self._matrice_adjacence[i][j], "\t", end="")
            print()
        if arete:
            print(self.aretes())
        print()

    def ajouter_arete(self, source, destination):
        """Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant."""
        checkType(source, int, destination, int)
        taille = len(self._matrice_adjacence)
        maximum = max(source, destination)
        if maximum >= taille:
            for u in range(maximum + 1):
                if u < taille:
                    for v in range(max(taille - maximum + 1, maximum - taille + 1)):
                        self._matrice_adjacence[u].append(0)
                else:
                    self._matrice_adjacence.append([0] * (max(taille + 1, maximum + 1)))
        if taille == 0:
            self._matrice_adjacence = [[0] * (maximum + 1) for _ in range(maximum + 1)]
        self._matrice_adjacence[source][destination] = 1
        self._matrice_adjacence[destination][source] = 1
        return

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels."""
        try:
            for (u, v) in iterable:
                self.ajouter_arete(u, v)
                self.ajouter_arete(v, u)
        except Exception:
            raise NameError(
                "L'iterable de la méthode ajouter_aretes n'est pas syntaxiquement correct : (u, v) par item")

    def ajouter_sommet(self):
        """Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = MatriceAdjacence()
        >>> G.ajouter_sommet()
        0
        >>> G._matrice_adjacence
        [[0]]
        >>> G.ajouter_sommet()
        1
        >>> G._matrice_adjacence
        [[0, 0], [0, 0]]
        """
        taille = len(self._matrice_adjacence)
        if taille == 0:
            self._matrice_adjacence.append([0])
        else:
            self._matrice_adjacence.append([])
            for i in range(taille):
                self._matrice_adjacence[i].append(0)
                self._matrice_adjacence[taille].append(0)
            self._matrice_adjacence[taille].append(0)
        return len(self._matrice_adjacence) - 1

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u))."""
        aretes = set()
        for i in range(len(self._matrice_adjacence)):
            for j in range(len(self._matrice_adjacence)):
                if self._matrice_adjacence[i][j]:
                    aretes.add((i, j))
        return aretes

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même."""
        boucles = []
        for i in range(len(self._matrice_adjacence)):
            for j in range(len(self._matrice_adjacence)):
                if self._matrice_adjacence[i][j] and i == j:
                    boucles.append((i, j))
        return boucles

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon."""
        checkType(u, int, v, int)
        for i in range(len(self._matrice_adjacence)):
            for j in range(len(self._matrice_adjacence)):
                if i == u and j == v and self._matrice_adjacence[u][v]:
                    return True
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        checkType(u, int)
        if 0 <= u < len(self._matrice_adjacence):
            return True
        return False

    def degre(self, sommet):
        """Renvoie le degré d'un sommet, c'est-à-dire le nombre de voisins
        qu'il possède."""
        checkType(sommet, int)
        if sommet < 0 or sommet > len(self._matrice_adjacence):
            raise NameError("Dans la méthode degre, le sommet n'existe pas.")
        nombre_sommet = 0
        for u in self._matrice_adjacence[sommet]:  # Ici les boucles sont considéré comme 1 degré
            if u:
                nombre_sommet += 1
        return nombre_sommet

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe."""
        from math import ceil
        nombre_aretes = 0
        for i in range(len(self._matrice_adjacence)):
            for j in range(len(self._matrice_adjacence)):
                if self._matrice_adjacence[i][j]:
                    nombre_aretes += 1
        return ceil(nombre_aretes / 2)

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}."""
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe.

        >>> from random import randint
        >>> n = randint(0, 1000)
        >>> MatriceAdjacence(n).nombre_sommets() == n
        True
        """
        return len(self._matrice_adjacence)

    def retirer_arete(self, u, v):
        """Retire l'arête {u, v} si elle existe; provoque une erreur sinon."""
        checkType(u, int, v, int)
        if u < 0 or u > len(self._matrice_adjacence) or v < 0 or v > len(self._matrice_adjacence):
            raise NameError(
                "Dans la méthode retirer_arete, l'arête n'est pas dans comprise le domaine de définition de la matrice.")
        if self._matrice_adjacence[u][v]:
            self._matrice_adjacence[u][v] = 0
            self._matrice_adjacence[v][u] = 0
            return
        raise NameError("Dans la méthode retirer_arete, l'arête n'est pas présente dans le graphe.")

    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        try:
            for (i, j) in iterable:
                self.retirer_arete(i, j)
        except Exception:
            raise NameError(
                "L'iterable de la méthode retirer_aretes n'est pas syntaxiquement correct : (u, v) par item")

    def retirer_sommet(self, sommet):
        """Déconnecte un sommet du graphe et le supprime."""
        checkType(sommet, int)
        taille = len(self._matrice_adjacence)
        if sommet < 0 or sommet >= taille:
            raise NameError("Le sommet n'est pas présent dans le graphe")
        else:
            for i in range(taille):
                self._matrice_adjacence[i].pop(sommet)
            self._matrice_adjacence.pop(sommet)

    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets."""
        try:
            taille = len(self._matrice_adjacence)
            statut = [0] * taille
            for i in iterable:
                self.retirer_sommet(i - statut[i])
                for j in range(i, taille):
                    statut[j] += 1
        except Exception:
            raise NameError("L'iterable de la méthode retirer_sommets n'est pas syntaxiquement correct : (u) par item")

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return {i for i in range(len(self._matrice_adjacence))}

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné."""
        try:
            sous_graphe = MatriceAdjacence(len(iterable))
            i = 0
            for u in sorted(iterable):
                j = 0
                for v in sorted(iterable):
                    if self._matrice_adjacence[u][v]:
                        sous_graphe.ajouter_arete(j, i)
                        sous_graphe.ajouter_arete(i, j)
                    j += 1
                i += 1
        except Exception:
            raise NameError(
                "L'iterable de la méthode sous_graphe_induit n'est pas syntaxiquement correct : (u) par item")
        return sous_graphe

    def voisins(self, sommet):
        """Renvoie la liste des voisins d'un sommet."""
        checkType(sommet, int)
        voisins = []
        for u in range(len(self._matrice_adjacence)):
            if self._matrice_adjacence[sommet][u]:
                voisins.append(u)
        return voisins


def export_dot(graphe):
    """Renvoie une chaîne encodant le graphe au format dot."""
    # from json import dumps
    # return dumps(graphe)
    texte = ""
    for i in range(graphe.nombre_sommets()):
        for j in range(i, graphe.nombre_sommets()):
            if graphe._matrice_adjacence[i][j]:
                texte += str(i) + " -- " + str(j) + ";\n"
    return texte


def main():
    import doctest
    doctest.testmod()

    graphe = MatriceAdjacence(0)
    for _ in range(5):
        print("Sommet ajouté", graphe.ajouter_sommet())
    graphe.affiche_matrice()
    graphe.ajouter_arete(0, 1)
    graphe.ajouter_arete(1, 10)
    graphe.ajouter_arete(10, 3)
    graphe.ajouter_aretes([(0, 1), (1, 5), (1, 5), (5, 1), (2, 3), (1, 2), (1, 4)])
    graphe.affiche_matrice(True)
    print(export_dot(graphe))
    print()

    graphe = MatriceAdjacence(0)
    graphe.ajouter_aretes(
        [(11, 1), (1, 1), (0, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 4), (4, 2),
         (4, 3), (4, 6), (5, 2), (5, 6), (5, 8), (5, 9), (6, 4), (6, 5), (6, 7), (7, 6), (8, 5), (8, 6), (8, 7),
         (8, 10), (9, 5), (9, 10), (10, 8), (10, 9)])
    graphe.affiche_matrice(True, False)

    print(graphe.sommets())
    print(graphe.nombre_sommets())
    print(graphe.aretes())
    print(graphe.nombre_aretes())
    print(graphe.boucles())
    print(graphe.nombre_boucles())
    print(graphe.degre(0))
    print(graphe.degre(1))
    print(graphe.degre(11))
    print(graphe.voisins(0))
    print(graphe.voisins(1))

    print(graphe.contient_arete(0, 0))
    print(graphe.contient_arete(1, 3))
    print(graphe.contient_arete(11, 1))
    print(graphe.contient_arete(11, 0))
    print(graphe.contient_sommet(0))
    print(graphe.contient_sommet(11))
    print(graphe.contient_sommet(12))

    # graphe.retirer_arete(0, 1)
    # graphe.retirer_arete(5, 8)
    # graphe.retirer_aretes([(1, 3), (2, 4), (2, 5), (2, 3), (9, 10)])
    # # graphe.retirer_arete(1, 3)  # Erreur puisque déjà retiré
    # graphe.affiche_matrice(True, False)

    # graphe.retirer_sommet(11)
    # graphe.retirer_sommet(0)
    # # graphe.retirer_sommet(0)
    # graphe.retirer_sommets((1, 2))
    # graphe.affiche_matrice(True, False)

    graphe.sous_graphe_induit((1, 2, 0, 5)).affiche_matrice()


if __name__ == "__main__":
    main()
