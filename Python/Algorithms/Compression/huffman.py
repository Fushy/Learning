from math import log


def count(L):
    dic = {}.fromkeys(L, 0)
    for valeur in L:
        dic[valeur] += 1
    return dic


class Heap:
    def __init__(self, function=lambda x: x):
        self.tab = []
        self.f = function

    def father(self, i):
        if i == 0:
            return None
        return int((i - 1) / 2)

    def left(self, i):
        if 2 * i + 1 < len(self.tab):
            return 2 * i + 1
        return None

    def right(self, i):
        if 2 * i + 2 < len(self.tab):
            return 2 * i + 2
        return None

    def __str__(self):
        return str(self.tab)

    def add(self, x):
        self.tab.append(x)
        i = len(self.tab) - 1
        while i > 0 and self.f(self.tab[i]) < self.f(self.tab[self.father(i)]):
            self.tab[i], self.tab[self.father(i)] = self.tab[self.father(i)], self.tab[i]
            i = self.father(i)

    def extract(self):
        if len(self.tab) == 1:
            return self.tab.pop()
        res = self.tab[0]
        self.tab[0] = self.tab.pop()
        i = 0
        while True:
            l, r = self.left(i), self.right(i)
            vl, vr = self.f(self.tab[i]), self.f(self.tab[i])
            if l is not None:
                vl = self.f(self.tab[l])
            if r is not None:
                vr = self.f(self.tab[r])
            if self.f(self.tab[i]) <= vr and self.f(self.tab[i]) <= vl:
                return res
            if vl < vr:
                self.tab[i], self.tab[l] = self.tab[l], self.tab[i]
                i = l
            else:
                self.tab[i], self.tab[r] = self.tab[r], self.tab[i]
                i = r


def huffmanTree(L):
    C = count(L)
    H = Heap(lambda x: x[0])
    for c in C:
        H.add(c)
    while len(H.tab) > 1:
        x1 = H.extract()
        x2 = H.extract()
        A = (x1[0] + x2[0], x1, x2)
        H.add(A)
    return H.tab[0]


def huffmanToCode(T, C=None, word=None):
    if word is None:
        word = []
    if C is None:
        C = {}
    if len(T) == 2:  # leaf
        C[T[1]] = u"".join(word)
    else:
        word.append('0')
        huffmanToCode(T[1], C, word)
        word[-1] = '1'
        huffmanToCode(T[2], C, word)
        word.pop()
    return C


def huffmanSize(text):
    arbre = huffmanTree(text)
    codage = huffmanToCode(arbre)
    k = len(codage)
    taille_arbre = (int(log(k + 1, 2) + 1) + 2) * k - 1
    taille_compression = sum([len(codage[l]) * nb for nb, l in count(text)])
    return taille_arbre + taille_compression
