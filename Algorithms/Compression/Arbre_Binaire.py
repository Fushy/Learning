class Arbre_Binaire:
	def __init__(self, lettre, poids, fils_gauche, fils_droit):
		self.lettre = lettre
		self.poids = poids
		self.fils_gauche = fils_gauche
		self.fils_droit = fils_droit
		# self.indent = indent

	def __str__(self):
		if self.fils_gauche is None or self.fils_droit is None:
			return "(" + str(self.lettre) + ":" + str(self.poids) + ")"
		return "(" + str(self.lettre) + ":" + str(self.poids) + " " + "(" + str(self.fils_gauche) + " ._. " + str(self.fils_droit) + "))"
