import copy


class ConnectedGraph:  # Structure permettant uniquement de manipuler les graphes connexe.
    def __init__(self, vertice):
        self.id = vertice
        self.neighbours = {}
        self.traveled = False

    def copy(self):
        return copy.deepcopy(self)


# class Vertice:   # Structure permettant de manipuler n'importe quel graphe. Non utilisé ici.
# 	def __init__ (self, id):
# 		self.id = id
# 		self.traveled = False
# class Graph:
# 	def __init__ (self, vertices, edges):
# 		self.vertices = [Vertice(u) for u in vertices]
# 		self.edges = edges
# 	def neighbours(self, vertice):
# 		neighbour = []
# 		for i,j in [u for u in self.edges if vertice in u]:
# 			if i != vertice:
# 				neighbour.append(i)
# 			if j != vertice:
# 				neighbour.append(j)
# 		return neighbour
# 	def copy(self):
# 		return copy.deepcopy(self)

# Affiche sur la console la liste des arêtes entré par l'utilisateur (afin de faire un copier coller au lieu de rentrer un par un les arêtes à la main, gain de temps).
def create_edges(weight=False):
    edges = {}
    print("u ...")
    u = input()
    while u != ".":
        print("v ...")
        v = input()
        if v == ".":
            print("u ...")
            u = input()
            continue
        if weight:
            print("p ...")
            w = input()
            edges[(int(u), int(v))] = int(w)
        else:
            edges[(int(u), int(v))] = 1
    print(":::", edges)
    return tuple(sorted(edges))


# Retourne les arêtes d'un graphe sans doublons ((u,v), (v,u)) et trié si le type de l'argument est une liste.
def optimise_edges(edges):
    if type(edges) == list:
        tmp = []
        for i, j in edges:
            if (i, j) not in tmp and (j, i) not in tmp:
                if i < j:
                    tmp.append((i, j))
                else:
                    tmp.append((j, i))
        return sorted(tmp)
    elif type(edges) == dict:
        tmp = {}
        for (i, j), p in edges.items():
            if (i, j) not in tmp and (j, i) not in tmp:
                if i < j:
                    tmp[(i, j)] = p
                else:
                    tmp[(j, i)] = p
        return tmp
    return type(edges)


# Met à 1 de poids toutes les arêtes de la liste G_edges.
def weighted_to_weighted1(edges):
    for i in G_edges.keys():
        G_edges[i] = 1
    return edges


# Met à 1 de poids toutes les arêtes de edges et retourne un dict.
def not_weighted_to_weighted1(edges):
    tmp = {}
    for i in edges:
        tmp[i] = 1
    return tmp


# Initialise un graphe connexe avec un nombre de sommet et des arêtes. Retourne le dict des sommets (sommet:voisins)
def init_connected_graph(vertices, edges, display=False):
    nodes = {}
    for i in vertices:
        nodes[i + 1] = ConnectedGraph(i + 1)
    for (u, v), p in edges.items():
        nodes[u].neighbours[nodes[v]] = p
        nodes[v].neighbours[nodes[u]] = p
    if display:
        for u in nodes:
            print(u, [str(i.id) + " |" + str(p) + "|" for i, p in nodes[u].neighbours.items()])
    return nodes


# Parcours en profondeur recursive (DFS) Depth-First Search, Affiche simplement le graph connexe d'un sommet donné.
def breath_first_search_rec(graph, node=1):
    def breath_first_search_rec_tmp(u):
        u.traveled = True
        # print("_", node.id, node.traveled, "_")
        for v in u.neighbours:
            if not v.traveled:
                breath_first_search_rec_tmp(v)

    vertice = graph[node].copy()
    breath_first_search_rec_tmp(vertice)


# Parcours en profondeur recursive avec une relation d'ordre et avec analyse des données.
# Retourne le nombre de sommet, nombre d'arêtes, poids du graph, arbre du parcours, les cycles obtenues grâce au parcours s'ils existent.
def data_graph(graph, node=1, display=False):
    def data_graph_tmp(vertice):
        # print("_", vertice.id, vertice.traveled, "_")
        nonlocal weight, edgecount
        if not vertice.traveled:
            vertice.traveled = True
            if display:
                print("_", vertice.id, vertice.traveled, "_")
        min = []
        for u, p in vertice.neighbours.items():  # Ajoute dans min le premier voisin qui n'a pas été parcouru.
            if not u.traveled:
                min.append(u)
                break
        if not min:  # Retourne la liste des pères si tous les voisins ont été parcouru.
            return fathers
        for u, p in vertice.neighbours.items():  # Ajoute dans min les voisins qui n'ont pas été parcouru
            if not u.traveled:
                edgecount += 1
                i = 0
                length = len(min)
                while i < length:  # Insertion dans min avec une relation d'ordre
                    if u.id < min[0].id:
                        min.insert(0, u)
                    elif u.id > min[length - 1].id:
                        min.append(u)
                    elif min[i].id < u.id < min[i + 1].id:
                        min.insert(i, u)
                    i += 1
            elif fathers[vertice] != u:
                cycle = [(u, vertice)]
                cursor = vertice
                while cursor != u:
                    cycle.append((cursor, fathers[cursor]))
                    cursor = fathers[cursor]
                cycleGraph.append(cycle)
            # print("cycle", [(u.id,v.id) for u,v in cycle])

        for u in min:  # Action pour chaque item dans min
            fathers[u] = vertice
            weight += vertice.neighbours[u]
            data_graph_tmp(u)  # Recommence pour chaque voisins non parcouru.
        return fathers  # Retourne la liste des pères si tous les voisins ont été parcouru. (Optionnel du coup car la condition à été vérifié plus haut)

    edgecount = 0
    fathers = {}
    weight = 0
    cycleGraph = []
    returnValue = data_graph_tmp(graph[node].copy())
    if display:
        print("fathers", [(u.id, v.id) for u, v in fathers.items()])
        print("weight", weight)
        print("cycleGraph", [[(u.id, v.id) for u, v in c] for c in cycleGraph])
    return len(fathers) + 1, edgecount, weight, [(u.id, v.id) for u, v in returnValue.items()], [
        [(u.id, v.id) for u, v in c] for c in cycleGraph]


# Parcours en largeur (BFS) breath_first_search
# Retourne la liste des distances du sommet donné en argument avec les autres sommet du graphe connexe, trié. (Si le graphe n'est pas connexe, ne renverra pas une distance infinie, ignorera juste.)
# Et retourne l'arbre de distance minimal
def breath_first_search(graph, node=1, display=False):
    checked = []
    fathers = {}
    vertice = graph[node].copy()
    dist = {(vertice.id, vertice.id): 0}  # Initialise la distance du sommet initiale avec lui même à 0.
    for u in vertice.neighbours:  # Pour chaque voisin, la distance entre le sommet initiale et le voisin est 1. On ajoute le voisin dans une liste s'il n'y est pas encore et s'il n'a pas déjà été parcouru.
        dist[(vertice.id, u.id)] = 1
        fathers[u.id] = vertice.id
        if not u.traveled and u not in checked:
            checked.append(u)
    vertice.traveled = True
    if display:
        print("_", vertice.id, vertice.traveled, "_")
    while checked:  # Tant que checked n'est pas vide, action sur chacun des voisin du premier item de checked
        u = checked[0]
        for v in u.neighbours:
            if not v.traveled and v not in checked:
                fathers[v.id] = u.id
                dist[(vertice.id, v.id)] = dist[(vertice.id, u.id)] + 1
                checked.append(v)
        u.traveled = True
        if display:
            print("_", u.id, u.traveled, "_")
        checked.remove(u)
    treeMinimal = optimise_edges([i for i in fathers.items()])
    if display:
        print("root", node)
        print("treeMinimal", treeMinimal)
        print("dist", sorted([(u, v) for u, v in dist.items()]))
    # elif type(graph) == Graph:
    # 	vertices = set()
    # 	vertice = graph.copy().vertices[node]
    # 	dist = {(vertice.id, vertice.id): 0}
    # 	for u in graph.neighbours(vertice.id):
    # 		vertices |= {u}
    # 		dist[(vertice.id, u)] = 1
    # 		fathers[u] = vertice.id
    # 		if not graph.vertices[u].traveled and u not in checked:
    # 			checked.append(u)
    # 			treeMinimal.append((vertice.id, u))
    # 	vertice.traveled = True
    # 	while checked:
    # 		u = checked[0]
    # 		for v in graph.neighbours(u):
    # 			vertices |= {u}
    # 			if not graph.vertices[v].traveled and v not in checked:
    # 				fathers[v] = u
    # 				dist[(vertice.id, v)] = dist[(vertice.id, u)] + 1
    # 				checked.append(v)
    # 				treeMinimal.append((u, v))
    # 		graph.vertices[u].traveled = True
    # 		checked.remove(u)
    # 	for i in {u.id for u in graph.vertices} - vertices - {0}:
    # 		dist[(node, i)] = float("inf")
    # 	if display:
    # 		print("root", node)
    # 		print("vertices", sorted(vertices))
    # 		print("father", sorted(fathers.items()))
    # 		print("treeMinimal", sorted([(u,v) for u,v in treeMinimal]))
    # 		print("dist", sorted([(u,v) for u,v in dist.items()]))
    # else:
    # 	return
    return dist, treeMinimal, [(sorted(i[0].items()), i[1]) for i in [[dist, treeMinimal]]][0]


# Retourne True si le graphe est biparti, False sinon
# Pas du tout optimisé
def is_bipartite(graph, edges, node=1, display=False):
    # if type(edges) == list:
    # 	dist = breath_first_search(graph.copy(), node=node)[0]
    # elif type(edges) == dict:
    tree = not_weighted_to_weighted1(dijkstra(graph.copy(), edges, node=node)[
                                         1])  # Transforme l'arbre des distances minimal d'un sommet donné du graphe en mettant tout ses poins à 1
    verticecount = {x for x in range(0, max([i for i, j in tree] + [j for i, j in tree]))}
    dist = breath_first_search(init_connected_graph(verticecount, tree, display=False), node=node)[
        0]  # On prend la liste des distances du parcours en largeur (avec un poids de 1 pour chaque arêtes).
    # else:
    # 	return type(edges)
    distColor = {}
    for edge, vertice in dist.items():
        if dist[edge] % 2 == 0:
            distColor[edge[1]] = "Blue"
        else:
            distColor[edge[1]] = "Red"
    if display:
        print(sorted(distColor.items()))
    for edge in edges:
        if display:
            print(edge, distColor[edge[0]], distColor[edge[1]])
        if edge[0] != edge[1] and distColor[edge[0]] == distColor[edge[1]]:
            return False
    return True


# Retourne la liste des distances du sommet donné en argument avec les autres sommet du graphe connexe pondéré, trié. Si le graphe est connexe, renverra une distance infinie.
# Et retourne l'arbre de distance minimal
# BFS d'un graphe pondéré.
def dijkstra(graph, edges, node=1, display=False):
    # Mets à jours les distances et retourne le prochain sommet qui doit être visité.
    def update_dist(vertice):
        if display:
            print("_", vertice.id, vertice.traveled, "_")
        # print("vertice.neighbours", vertice.id, sorted([(u.id,p) for u,p in vertice.neighbours.items()]))
        for _, u, p in sorted([(u.id, u, p) for u, p in
                               vertice.neighbours.items()]):  # Mise à jours des distances et ajout dans checked les sommets accessible à partir du sommet initiale s'il ne l'etait pas.
            if u not in checked:
                checked.append(u)
            if dist[root.id, u.id] > dist[root.id, vertice.id] + p:
                dist[root.id, u.id] = dist[root.id, vertice.id] + p
                fathers[u] = vertice
            # if display:
            # 	print("\tUpdate", {(root.id, u.id): dist[root.id, u.id]})
            # 	print("\tfathers", [(u.id,v.id) for u,v in fathers.items()])
            # 	print("\t", dist)
        vertice.traveled = True
        mini = 0
        for u in checked:
            if not u.traveled:
                mini = u, dist[(root.id, u.id)]
                break
        if mini:
            for u in checked:
                if not u.traveled and dist[(root.id, u.id)] < dist[(root.id, mini[
                    0].id)]:  # Retourne la distance minimal entre le sommet root et les sommets de la liste checked.
                    mini = u, dist[(root.id, u.id)]
        if not mini:  # Retourne [root] si tous les sommets de checked ont déjà été parcouru
            return [root]
        # if display:
        # 	print("Min", mini[0].id)
        return mini

    dist = {}
    fathers = {}
    checked = []
    for (u, v), p in edges.items():  # Initialise toute les distances du sommet initiale avec les sommets du graphe à 0.
        dist[(node, u)] = float("inf")
        dist[(node, v)] = float("inf")
    dist[(node, node)] = 0  # Initialise la distance du sommet initiale avec lui même à 0.
    root = graph[node].copy()
    checked.append(root)
    returnValue = update_dist(root)
    while not returnValue[0].traveled:  # Mets à jours les distances tant que tous les sommets n'ont pas été parcouru
        returnValue = update_dist(returnValue[0])
    treeMinimal = optimise_edges([(i.id, j.id) for i, j in fathers.items()])
    return dist, treeMinimal, [(sorted(i[0].items()), i[1]) for i in [[dist, treeMinimal]]][0]


# Permet d'obtenir un arbre couvrant de poids minimal d'un graphe pondéré connexe.
# Retourne l'arbre couvrant de poids minimal et le poids de l'arbre
def prim(graph, node=1, display=False):
    fathers = {}
    checked = []
    weight = 0
    vertice = graph[node].copy()
    while 1:
        if display:
            print("__", vertice.id, "__")
        min = 0
        vertice.traveled = True
        for u, p in vertice.neighbours.items():  # Ajoute dans checked les voisins du sommet en train d'être parcouru
            checked.append((vertice, u, p))
        for u, v, p in checked:  # On cherche l'arête qui possède le poids minimal parmi les sommets présent dans checked
            if not v.traveled:
                min = (u, v, p)
                break
        if not min:  # Si tout les sommets voisins ont été parcouru
            return weight, sorted([(u.id, v.id) for u, v in fathers.items()])
        for u, v, p in checked:  # Trouve l'arête de poids minimal
            if not v.traveled and p < min[2]:
                min = (u, v, p)
        for u, v, p in checked:  # Trouve l'arête de poids et de id minimal
            if not v.traveled and p == min[2] and u.id < min[0].id:
                min = (u, v, p)
        if display:
            print("Min (", min[0].id, ",", min[1].id, ") :", min[2])
        # On actualise les données grâce à l'arête de poids minimal trouvée
        weight += min[2]
        fathers[min[1]] = min[0]
        vertice = min[1]


#####################
sommetInitial = 5
#####################

# create_edges(True)
# create_edges(False)
# vertices = {x:chr(ord('A')+x) for x in range(11)}
# G_edges = [(1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 4), (4, 2), (4, 3), (4, 6), (5, 2), (5, 6), (5, 8), (5, 9), (6, 4), (6, 5), (6, 7), (7, 6), (7, 11), (8, 5), (8, 6), (8, 7), (8, 10), (9, 5), (9, 10), (10, 8), (10, 9), (11, 7)]
# G_edges = [(1, 2), (1, 3), (1, 4), (2, 1), (2, 5), (2, 6), (3, 1), (3, 5), (3, 7), (4, 1), (4, 6), (4, 8), (5, 2), (5, 3), (5, 9), (6, 2), (6, 4), (6, 9), (7, 3), (7, 10), (8, 4), (8, 10), (9, 5), (9, 6), (9, 11), (10, 7), (10, 8), (10, 11), (11, 9), (11, 10)]
# G_edges = [(1, 3), (1, 5), (1, 6), (1, 7), (2, 4), (2, 5), (2, 9), (3, 1), (3, 4), (4, 2), (4, 3), (4, 8), (5, 1), (5, 2), (6, 1), (6, 9), (7, 1), (7, 8), (8, 4), (8, 7), (8, 9), (9, 2), (9, 6), (9, 8)]
# G_edges = not_weighted_to_weighted1(G_edges)
# G_edges = {(1, 4): 9, (1, 6): 1, (1, 8): 1, (2, 5): 5, (2, 4): 2, (2, 6): 10, (3, 4): 3, (3, 5): 7, (3, 7): 2, (4, 3): 3, (4, 2): 2, (4, 1): 9, (4, 8): 4, (5, 2): 5, (5, 3): 7, (6, 2): 10, (6, 1): 1, (7, 3): 2, (7, 8): 2, (8, 1): 1, (8, 4): 4, (8, 7): 2}
# G_edges = {(1, 2): 1, (1, 7): 1, (1, 3): 1, (2, 1): 1, (2, 7): 1, (2, 6): 1, (2, 4): 1, (3, 4): 1, (3, 1): 1, (4, 3): 1, (4, 2): 1, (4, 5): 1, (5, 4): 1, (5, 6): 1, (5, 9): 1, (6, 2): 1, (6, 8): 1, (6, 5): 1, (7, 2): 1, (7, 1): 1, (8, 6): 1, (8, 9): 1, (9, 8): 1, (9, 5): 1}
G_edges = {(1, 2): 10, (1, 9): 11, (2, 1): 10, (2, 3): 5, (2, 7): 9, (3, 2): 5, (3, 9): 5, (3, 4): 3, (3, 5): 4,
           (4, 3): 3, (4, 5): 4, (4, 11): 10, (4, 10): 5, (5, 3): 4, (5, 7): 2, (5, 6): 1, (5, 4): 4, (6, 8): 4,
           (6, 5): 1, (6, 7): 3, (7, 6): 3, (7, 5): 2, (7, 2): 9, (8, 6): 4, (8, 11): 8, (10, 4): 5, (10, 9): 9,
           (11, 8): 8, (11, 4): 10}
G_edges = optimise_edges(G_edges)

G_vertices = {x for x in range(0, max([i for i, j in G_edges] + [j for i, j in G_edges]))}

print("Sommets :", sorted(G_vertices))
print("Arcs :", G_edges)
connectedGraph = init_connected_graph(G_vertices, G_edges, display=False)
print("(|Sommets|, |Arcs|, Weight, Arcs, Cycles) :", data_graph(connectedGraph, sommetInitial, display=False))
print("__.__")

breath_first_search_rec(connectedGraph, sommetInitial)

print(breath_first_search(connectedGraph, sommetInitial, display=False)[2])
print(dijkstra(connectedGraph, G_edges, sommetInitial, display=False)[2])

print(is_bipartite(connectedGraph, G_edges, sommetInitial, display=False))

print(prim(connectedGraph, sommetInitial, display=False))
