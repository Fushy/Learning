# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe à l'aide d'une liste d'adjacence. Les n sommets
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


class ListeAdjacence(object):
    def __init__(self, num=0):
        """Initialise un graphe sans arêtes sur num sommets.

        >>> G = ListeAdjacence()
        >>> G._liste_adjacence
        []
        """
        self._liste_adjacence = [list() for _ in range(num)]

    def affiche_liste(self, arete=False):
        print(self._liste_adjacence)
        if arete:
            print(self.aretes())

    def ajouter_arete(self, source, destination):
        """Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant.

            De plus effectue une insertion logique et empêche les doublons. Autorise le sommet 0."""
        checkType(source, int, destination, int)
        maximum = max(source, destination)
        if maximum > len(self._liste_adjacence) - 1:
            for _ in range(len(self._liste_adjacence), maximum + 1):
                self._liste_adjacence.append([])
        for u, v, taille in [(source, destination, len(self._liste_adjacence[source])),
                             (destination, source, len(self._liste_adjacence[destination]))]:
            if taille == 0:
                self._liste_adjacence[u].append(v)
                continue
            i = 0
            while i < taille:  # Insertion dans self._liste_adjacence[source] avec une relation d'ordre
                if v < self._liste_adjacence[u][0]:
                    self._liste_adjacence[u].insert(0, v)
                    break
                elif v > self._liste_adjacence[u][taille - 1]:
                    self._liste_adjacence[u].append(v)
                    break
                elif self._liste_adjacence[u][i] < v < self._liste_adjacence[u][
                    i + 1]:  # Insertion et empêche les doublons
                    self._liste_adjacence[u].insert(i + 1, v)
                    break
                i += 1

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels."""
        try:
            for (u, v) in iterable:
                self.ajouter_arete(u, v)
        except Exception:
            raise NameError(
                "L'iterable de la méthode ajouter_aretes n'est pas syntaxiquement correct : (u, v) par item")

    def ajouter_sommet(self):
        """Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = ListeAdjacence()
        >>> G.ajouter_sommet()
        0
        >>> G._liste_adjacence
        [[]]
        >>> G.ajouter_sommet()
        1
        >>> G._liste_adjacence
        [[], []]
        """
        self._liste_adjacence.append([])
        return len(self._liste_adjacence) - 1

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u))."""
        aretes = set()
        u = 0
        for sommet_curseur in self._liste_adjacence:
            for v in sommet_curseur:
                # if u != v: # Ignore les boucles
                aretes.add((u, v))
            u += 1
        return aretes

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même."""
        boucles = []
        u = 0
        for sommet_curseur in self._liste_adjacence:
            for v in sommet_curseur:
                if u == v:
                    boucles.append((u, v))
            u += 1
        return boucles

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon."""
        checkType(u, int, v, int)
        u_curseur = 0
        for sommet_curseur in self._liste_adjacence:
            for v_curseur in sommet_curseur:
                if u_curseur == u and v_curseur == v:
                    return True
            u_curseur += 1
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        checkType(u, int)
        # try:
        #     self._liste_adjacence[u]
        #     return True
        # except Exception:
        #     return False
        if 0 <= u < len(self._liste_adjacence):
            return True
        return False

    def degre(self, sommet):
        """Renvoie le degré d'un sommet, c'est-à-dire le nombre de voisins
        qu'il possède."""
        checkType(sommet, int)
        if self.contient_sommet(sommet):
            return len(self._liste_adjacence[sommet])
        raise NameError("Dans la méthode degre, le sommet n'existe pas.")

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe."""
        from math import ceil
        nombre_aretes = 0
        for sommet_curseur in self._liste_adjacence:
            nombre_aretes += len(sommet_curseur)
        return ceil(nombre_aretes / 2)

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}."""
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe.

         >>> from random import randint
         >>> n = randint(0, 1000)
         >>> ListeAdjacence(n).nombre_sommets() == n
         True
        """
        return len(self._liste_adjacence)

    def retirer_arete(self, u, v):
        """Retire l'arête {u, v} si elle existe; provoque une erreur sinon."""
        checkType(u, int, v, int)
        u_curseur = 0
        for sommet_curseur in self._liste_adjacence:
            for v_curseur in sommet_curseur:
                if u_curseur == u and v_curseur == v:
                    self._liste_adjacence[u].remove(v)
                    self._liste_adjacence[v].remove(u)
                    return
            u_curseur += 1
        raise NameError("Dans la méthode retirer_arete, l'arête n'est pas présente dans le graphe.")

    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        try:
            for (u, v) in iterable:
                self.retirer_arete(u, v)
        except Exception:
            raise NameError(
                "L'iterable de la méthode retirer_aretes n'est pas syntaxiquement correct : (u, v) par item")

    def retirer_sommet(self, sommet):
        """Déconnecte un sommet du graphe et le supprime."""
        checkType(sommet, int)
        taille = len(self._liste_adjacence)
        if sommet < 0 or sommet >= taille:
            raise NameError("Le sommet n'est pas présent dans le graphe")
        self._liste_adjacence.remove(self._liste_adjacence[sommet])
        for u in self._liste_adjacence:
            if sommet in u:
                u.remove(sommet)
            i = 0
            for v in u:
                if sommet < v:
                    u[i] = u[
                               i] - 1  # Permet d'actualiser les sommets du graphe afin que les sommets correspondent bien à leur emplacement dans la liste.
                i += 1

    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets."""
        try:
            for u in iterable:
                self.retirer_sommet(u)
        except Exception:
            raise NameError("L'iterable de la méthode retirer_sommets n'est pas syntaxiquement correct : (u) par item")

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return {i for i in range(len(self._liste_adjacence))}

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné."""
        sous_graphe = ListeAdjacence(0)
        try:
            u = 0
            for sommet in sorted(iterable):
                sous_graphe.ajouter_sommet()
                for v in sorted(self._liste_adjacence[sommet]):
                    if v in iterable and v not in sous_graphe._liste_adjacence[u]:
                        sous_graphe._liste_adjacence[u].append(v)
                u += 1

                # sous_graphe.self._liste_adjacence[]
        except Exception:
            raise NameError(
                "L'iterable de la méthode sous_graphe_induit n'est pas syntaxiquement correct : (u) par item")
        return sous_graphe

    def voisins(self, sommet):
        """Renvoie la liste des voisins d'un sommet."""
        checkType(sommet, int)
        return self._liste_adjacence[sommet]


def main():
    import doctest
    doctest.testmod()

    graphe = ListeAdjacence(0)
    for _ in range(5):
        print("Sommet ajouté", graphe.ajouter_sommet())
    graphe.affiche_liste()
    graphe.ajouter_arete(0, 1)
    graphe.ajouter_arete(1, 10)
    graphe.ajouter_arete(10, 3)
    graphe.ajouter_aretes([(0, 1), (1, 5), (1, 5), (5, 1), (2, 3), (1, 2), (1, 4)])
    graphe.affiche_liste(True)
    print()

    graphe = ListeAdjacence(0)
    graphe.ajouter_aretes(
        [(11, 1), (1, 1), (0, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 4), (4, 2),
         (4, 3), (4, 6), (5, 2), (5, 6), (5, 8), (5, 9), (6, 4), (6, 5), (6, 7), (7, 6), (8, 5), (8, 6), (8, 7),
         (8, 10), (9, 5), (9, 10), (10, 8), (10, 9)])
    graphe.affiche_liste()

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
    # graphe.affiche_liste()

    # graphe.retirer_sommet(11)
    # graphe.retirer_sommet(0)
    # # graphe.retirer_sommet(0)
    # graphe.retirer_sommets((1, 2))
    # graphe.affiche_liste()

    # graphe.sous_graphe_induit((1, 2, 0, 5)).affiche_liste()


if __name__ == "__main__":
    main()
