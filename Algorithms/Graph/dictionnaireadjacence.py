#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe orienté à l'aide d'un dictionnaire: les clés
sont les sommets, et les valeurs sont les sommets adjacents à un sommet donné.
Les boucles sont autorisées. Les poids ne sont pas autorisés.

On utilise la représentation la plus simple:
    un arc {u, v} sera présente
    une fois dans le dictionnaire: v est dans l'ensemble des voisins de u.

    une arête {u, v} sera présente
    deux fois dans le dictionnaire: v est dans l'ensemble des voisins de u, et u
    est dans l'ensemble des voisins de v.
    Une arête (u, v) représente donc un arc (u, v) et (v, u).

"""


class DictionnaireAdjacence(object):
    def __init__(self):
        """Initialise un graphe sans arêtes"""
        self.dictionnaire = dict()

    def affiche_dictionnaire(self):
        """Permet l'affichage du dictionnaire à titre d'information, les clés ne sont plus des set mais des list afin de visualiser par ordre croissant."""
        dictionnaire = "{"
        for k, v in sorted(self.dictionnaire.items()):
            dictionnaire += str(k) + ": " + str(sorted(v)) + ", "
        dictionnaire = list(dictionnaire)
        dictionnaire[-2:-1] = "}"
        print("".join(dictionnaire))

    def ajouter_arete(self, u, v):
        """Ajoute une arête entre les sommmets u et v, en créant les sommets
        manquants le cas échéant."""
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.dictionnaire[v] = set()
        # ajout de u (resp. v) parmi les voisins de v (resp. u)
        self.dictionnaire[u].add(v)
        self.dictionnaire[v].add(u)

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v in iterable:
            self.ajouter_arete(u, v)

    def ajouter_sommet(self, sommet):
        """Ajoute un sommet (de n'importe quel type hashable) au graphe."""
        if sommet not in self.dictionnaire:
            self.dictionnaire[sommet] = set()

    def ajouter_sommets(self, iterable):
        """Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables."""
        for sommet in iterable:
            self.ajouter_sommet(sommet)

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe. Une arête est représentée
        par un tuple (a, b) avec a <= b afin de permettre le renvoi de boucles.
        """
        return {
            tuple(sorted((u, v))) for u in self.dictionnaire
            for v in self.dictionnaire[u]
        }

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même."""
        return {(u, u) for u in self.dictionnaire if u in self.dictionnaire[u]}

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon."""
        if self.contient_sommet(u) and self.contient_sommet(v):
            return u in self.dictionnaire[v]  # ou v in self.dictionnaire[u]
        return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon."""
        return u in self.dictionnaire

    def degre(self, sommet):
        """Renvoie le nombre de voisins du sommet; s'il n'existe pas, provoque
        une erreur."""
        return len(self.dictionnaire[sommet])

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe."""
        # attention à la division par 2 (chaque arête étant comptée deux fois)
        return sum(len(voisins) for voisins in self.dictionnaire.values()) // 2

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}."""
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe."""
        return len(self.dictionnaire)

    def retirer_arete(self, u, v):
        """Retire l'arête {u, v} si elle existe; provoque une erreur sinon."""
        self.dictionnaire[u].remove(v)  # plante si u ou v n'existe pas
        self.dictionnaire[v].remove(u)  # plante si u ou v n'existe pas

    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple)."""
        for u, v in iterable:
            self.retirer_arete(u, v)

    def retirer_sommet(self, sommet):
        """Efface le sommet du graphe, et retire toutes les arêtes qui lui
        sont incidentes."""
        del self.dictionnaire[sommet]
        # retirer le sommet des ensembles de voisins
        for u in self.dictionnaire:
            self.dictionnaire[u].discard(sommet)

    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets."""
        for sommet in iterable:
            self.retirer_sommet(sommet)

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe."""
        return set(self.dictionnaire.keys())

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné."""
        G = DictionnaireAdjacence()
        G.ajouter_sommets(iterable)
        for u, v in self.aretes():
            if G.contient_sommet(u) and G.contient_sommet(v):
                G.ajouter_arete(u, v)
        return G

    def voisins(self, sommet):
        """Renvoie l'ensemble des voisins du sommet donné."""
        return self.dictionnaire[sommet]

    def ajouter_arc(self, u, v):
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.dictionnaire[v] = set()
        # ajout de v parmi les voisins de u
        self.dictionnaire[u].add(v)

    def ajouter_arcs(self, iterable):
        for u, v in iterable:
            self.ajouter_arc(u, v)

    def arcs(self):
        return {(u, v) for u in self.dictionnaire for v in self.dictionnaire[u]}

    def contient_arc(self, u, v):
        if (u, v) in self.arcs(): return True
        return False

    def degre_entrant(self, sommet):
        degre_entrant = 0
        for u in self.dictionnaire:
            if sommet in self.dictionnaire[u]:
                degre_entrant += 1
        return degre_entrant

    def degre_sortant(self, sommet):
        return len(self.dictionnaire[sommet])

    def nombre_arcs(self):
        return len(self.arcs())

    def predecesseurs(self, sommet):
        predecesseurs = set()
        for u in self.dictionnaire:
            if sommet in self.dictionnaire[u]:
                predecesseurs.add(u)
        return predecesseurs

    def successeurs(self, sommet):
        return {u for u in self.dictionnaire[sommet]}

    def retirer_arc(self, u, v):
        self.dictionnaire[u].remove(v)
        # if len(self.dictionnaire[u]) == 0:
        #     del self.dictionnaire[u]  # Ne pas supprimer afin de garder une taille correspondant au nombre de sommet

    def retirer_arcs(self, iterable):
        for u, v in iterable:
            self.retirer_arc(u, v)


def foret_profondeur(graphe):
    def parcours_recursif_connexe(u, texte):
        est_parcouru.add(u)
        nouveau_graphe.ajouter_sommet(noeud)
        for v in sorted(graphe.voisins(u)):
            if v not in est_parcouru:
                nouveau_graphe.ajouter_arc(u, v)
                texte.append(str(v))
                texte.append(" -> ")
                parcours_recursif_connexe(v, texte)
        return texte

    if type(graphe) != DictionnaireAdjacence:
        return type(graphe)()
    nouveau_graphe = DictionnaireAdjacence()
    est_parcouru = set()
    affichage = []
    while len(est_parcouru) < graphe.nombre_sommets():
        noeud = sorted((graphe.sommets() - est_parcouru))[0]
        affichage.append(parcours_recursif_connexe(noeud, [str(noeud), " -> "]))
    # print(["".join(u) for u in affichage])  # Affiche les différentes foret du parcours
    # print(["".join(["".join(u) for u in affichage])][0][:-4])  # Affiche le parcours
    return nouveau_graphe


def foret_largeur(graphe):
    def parcours_largeur_connexe(noeud):
        est_parcouru.add(noeud)
        nouveau_graphe.ajouter_sommet(noeud)
        texte = [str(noeud), " -> "]
        a_parcourir = []
        for u in sorted(graphe.voisins(noeud)):
            if u not in est_parcouru and u not in a_parcourir:
                a_parcourir.append(u)
                nouveau_graphe.ajouter_arc(noeud, u)
        while a_parcourir:
            u = a_parcourir[0]
            for v in sorted(graphe.voisins(u)):
                if v not in est_parcouru and v not in a_parcourir:
                    a_parcourir.append(v)
                    nouveau_graphe.ajouter_arc(u, v)
            est_parcouru.add(u)
            a_parcourir.remove(u)
            texte.append(str(u))
            texte.append(" -> ")
        return texte

    if type(graphe) != DictionnaireAdjacence:
        return type(graphe)()
    nouveau_graphe = DictionnaireAdjacence()
    est_parcouru = set()
    affichage = []
    while len(est_parcouru) < graphe.nombre_sommets():
        affichage.append(parcours_largeur_connexe(sorted((graphe.sommets() - est_parcouru))[0]))
    # print(["".join(u) for u in affichage])  # Affiche les différentes foret du parcours
    # print(["".join(["".join(u) for u in affichage])][0][:-4])  # Affiche le parcours
    return nouveau_graphe


def cycle_profondeur(graphe):
    def parcours_recursif_connexe(u):
        est_parcouru.add(u)
        for v in sorted(graphe.voisins(u)):
            if v not in est_parcouru:
                pere[v] = u
                parcours_recursif_connexe(v)
            elif v in pere:
                cycle = [(u, v)]
                curseur = u
                while curseur != v:
                    if curseur in pere:
                        cycle.append((pere[curseur], curseur))
                        curseur = pere[curseur]
                    else:
                        cycle = []
                        break
                if cycle:
                    nouveau_graphe.ajouter_arcs(cycle)
                    cycleGraph.append(cycle)
        return

    if type(graphe) != DictionnaireAdjacence:
        return type(graphe)()
    nouveau_graphe = DictionnaireAdjacence()
    pere = {}
    cycleGraph = []
    est_parcouru = set()
    while len(est_parcouru) < graphe.nombre_sommets():
        noeud = sorted((graphe.sommets() - est_parcouru))[0]
        parcours_recursif_connexe(noeud)
    # print(sorted(pere.items())) # Affiche le tableau des peres
    # print(cycleGraph)   # Affiche les cycles
    return nouveau_graphe


def cycle_largeur(graphe):
    def parcours_largeur_connexe(noeud):
        est_parcouru.add(noeud)
        a_parcourir = []
        for u in sorted(graphe.voisins(noeud)):
            if u not in pere:
                pere[u] = noeud
            if u not in est_parcouru and u not in a_parcourir:
                a_parcourir.append(u)
        while a_parcourir:
            u = a_parcourir[0]
            for v in sorted(graphe.voisins(u)):
                if v not in pere:
                    pere[v] = u
                if v not in est_parcouru and v not in a_parcourir:
                    a_parcourir.append(v)
                elif u in pere:
                    cycle = [(u, v)]
                    curseur = u
                    while curseur != v:
                        if curseur in pere:
                            cycle.append((pere[curseur], curseur))
                            curseur = pere[curseur]
                        else:
                            cycle = []
                            break
                    if cycle:
                        nouveau_graphe.ajouter_arcs(cycle)
                        cycleGraph.append(cycle)
            est_parcouru.add(u)
            a_parcourir.remove(u)
        return

    if type(graphe) != DictionnaireAdjacence:
        return type(graphe)()
    nouveau_graphe = DictionnaireAdjacence()
    pere = {}
    cycleGraph = []
    est_parcouru = set()
    while len(est_parcouru) < graphe.nombre_sommets():
        parcours_largeur_connexe(sorted((graphe.sommets() - est_parcouru))[0])
    # print(sorted(pere.items())) # Affiche le tableau des peres
    # print(cycleGraph)   # Affiche les cycles
    return nouveau_graphe


def main():
    graphe = DictionnaireAdjacence()
    graphe.ajouter_arcs(
        [(1, 2), (1, 4), (2, 4), (3, 2), (5, 7), (5, 10), (5, 11), (6, 5), (9, 14), (10, 9), (11, 7), (12, 7), (12, 13),
         (13, 2), (13, 8), (14, 10)])
    print("Dictionnaire du graphe :\n", end=" ");
    graphe.affiche_dictionnaire();
    print()
    # print(sorted(graphe.arcs()))
    # print(graphe.contient_arc(1, 1))
    # print(graphe.contient_arc(1, 2))
    # print(graphe.contient_arc(8, 9))
    # print(graphe.nombre_arcs())
    # print(graphe.predecesseurs(1))
    # print(graphe.degre_entrant(1))
    # print(graphe.successeurs(1))
    # print(graphe.degre_sortant(1))
    # print(graphe.predecesseurs(9))
    # print(graphe.degre_entrant(9))
    # # print(graphe.degre_sortant(9))
    # print(graphe.predecesseurs(5))
    # print(graphe.degre_entrant(5))
    # print(graphe.degre_sortant(5))
    # print(graphe.successeurs(5))
    # graphe.retirer_arcs(((1, 2), (1, 4), (13, 8)))
    # graphe.affiche_dictionnaire()

    print("Parcours profondeur :\n", end=" ");
    foret_profondeur(graphe).affiche_dictionnaire();
    print()
    print("Parcours foret_largeur :\n", end=" ");
    foret_largeur(graphe).affiche_dictionnaire();
    print()
    print("Cycle profondeur :\n", end=" ");
    cycle_profondeur(graphe).affiche_dictionnaire();
    print()
    print("Cycle largeur :\n", end=" ");
    cycle_largeur(graphe).affiche_dictionnaire();
    print()


if __name__ == "__main__":
    main()
