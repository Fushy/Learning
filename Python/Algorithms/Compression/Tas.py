# 2

class Tas:
	def __init__(self, cle = lambda x:x):
		self.table = []                     # Sous forme [(str_lettre, int_compteur), ...]
		self.taille = 0
		self.relation_ordre = cle

	def __str__(self):
		return str(self.table)

	def pere(self, i):
		if i == 0:
			return None
		return int((i-1) / 2)

	def fils_gauche_valeur(self, i):
		if 2*i+1 < len(self.table):
			return 2*i + 1
		return None

	def fils_droit_valeur(self, i):
		if 2*i+2 < len(self.table):
			return 2*i + 2
		return None

	def ajout(self, valeur):
		self.table.append(valeur)
		index = self.taille
		self.taille += 1
		while index > 0:
			pere_index = self.pere(index)
			pere = self.table[pere_index]
			if self.relation_ordre(pere) <= self.relation_ordre(valeur):
				break
			else:
				self.table[index], self.table[pere_index] = pere, valeur    # Echange
				index = pere_index

	def extraire(self):
		def echange_noeud(index):
			curseur = self.table[index]
			fils_gauche_index = self.fils_gauche_valeur(index)
			fils_droit_index = self.fils_droit_valeur(index)
			if fils_gauche_index is not None:
				fils_gauche_valeur = self.table[fils_gauche_index]
			else:
				fils_gauche_valeur = None
			if fils_droit_index is not None:
				fils_droit_valeur = self.table[fils_droit_index]
			else:
				fils_droit_valeur = None

			if fils_droit_index is not None:                                                        # Si le curseur possède un fils droit
				if self.relation_ordre(fils_gauche_valeur) < self.relation_ordre(curseur) and self.relation_ordre(fils_gauche_valeur) <= self.relation_ordre(fils_droit_valeur):
					self.table[fils_gauche_index], self.table[index] = curseur, fils_gauche_valeur  # Echange
					echange_noeud(fils_gauche_index)                                                # Recommence
				elif self.relation_ordre(fils_droit_valeur) < self.relation_ordre(curseur) and self.relation_ordre(fils_droit_valeur) <= self.relation_ordre(fils_gauche_valeur):
					self.table[fils_droit_index], self.table[index] = curseur, fils_droit_valeur    # Echange
					echange_noeud(fils_droit_index)                                                 # Recommence
			elif fils_gauche_index is not None:                                                     # Si le curseur ne possède pas de fils droit mais possède un fils gauche
				if self.relation_ordre(fils_gauche_valeur) < self.relation_ordre(curseur):
					self.table[fils_gauche_index], self.table[index] = curseur, fils_gauche_valeur  # Echange
		########################
		if len(self.table) == 0:
			return None
		self.taille -= 1
		if len(self.table) == 1:
			return self.table.pop()
		valeur_supprime = self.table[0]
		self.table[0] = self.table.pop()
		if self.taille > 0:
			echange_noeud(0)
		return valeur_supprime

	def extraire_tout(self):
		print(self)
		while len(self.table):
			print("-", self.extraire())
			print(self)

# 3
def tri_tas(valeurs, cle = lambda x:x):
	tas_local = Tas(cle)
	for valeur in valeurs:
		tas_local.ajout(valeur)

	liste_trie = []
	while tas_local.taille > 0:
		liste_trie.append(tas_local.extraire())
	return liste_trie