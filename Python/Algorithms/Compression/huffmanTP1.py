from random import *
from Tas import *
from Arbre_Binaire import *
from ByteEncoder import *

# 1
def count(texte):
	return sorted([(texte.count(caractere), caractere) for caractere in set(texte)], reverse=True)

# 4
def huffmanTree(doublets):
	tas_local = Tas(lambda a : a.poids)
	for valeur, poids in doublets:
		tas_local.ajout(Arbre_Binaire(valeur, poids, None, None))   # Ajout dans un tas la liste des arbres sans fils avec comme relation d'ordre le poids
	while tas_local.taille > 1:     # Tant qu'il y a plus d'un arbre dans le tas (tant que le tas ne se resume pas à sa racine), extraire les 2 minimums afin de créer un nouvel arbre
		fils_gauche = tas_local.extraire()
		fils_droit = tas_local.extraire()
		nouvel_arbre = Arbre_Binaire('', fils_gauche.poids + fils_droit.poids, fils_gauche, fils_droit)
		tas_local.ajout(nouvel_arbre)
	return tas_local.table[0]       # On retourne la racine

# 5
def huffmanToCode(arbre):
	def code_sous_arbre(code, noeud):
		if noeud.fils_gauche:
			liste_nouvelle_memoire1 = list(code)
			liste_nouvelle_memoire1.append(0)
			code_sous_arbre(liste_nouvelle_memoire1, noeud.fils_gauche)
		if noeud.fils_droit:
			liste_nouvelle_memoire2 = list(code)
			liste_nouvelle_memoire2.append(1)
			code_sous_arbre(liste_nouvelle_memoire2, noeud.fils_droit)
		if noeud.lettre is not None:
			codage[noeud.lettre] = code
	#################################
	codage = {}
	code_sous_arbre([], arbre)
	return codage

# 6
def applyCode(code, mot):
	codage = []
	for caractere in mot:
		codage.append(code[caractere])
	code_binaire = []
	for liste in codage:
		for bit in liste:
			code_binaire += str(bit)
	code_binaire_compacte = "".join(code_binaire)
	# return codage
	return code_binaire_compacte

# 7
def calcul_taux_compression(texte):
	dictionnaire_de_mot = count(texte)
	arbre_huffman = huffmanTree(dictionnaire_de_mot)
	codage_arbre_huffman = huffmanToCode(arbre_huffman)
	compression = applyCode(codage_arbre_huffman, texte)
	taille_initiale = len(texte)
	taille_compression = len(compression) / 8
	taux = taille_compression / taille_initiale * 100
	# print("dictionnaire_de_mot", dictionnaire_de_mot)
	# print("arbre_huffman", arbre_huffman)
	# print("codage_arbre_huffman", codage_arbre_huffman)
	# print("compression", compression)
	# print("taille_initiale", taille_initiale)
	# print("taille_compression", taille_compression)
	# encodeTree(arbre_huffman)
	gain = 100 - taux
	return taux

# 9
# ...
def encodeTree(arbre_huffman):
	encodage_arbre_huffman = ByteEncoder([], [])
	encodage_arbre_huffman.addString(str(arbre_huffman))
	encodage_arbre_huffman.write("encodage_arbre_huffman.txt")

# 10
# ...
def HuffmanEncoding(fichier_lecture, fichier_ecriture):
	fichier_lecture = open(fichier_lecture, 'rb')
	texte = fichier_lecture.read()
	dictionnaire_de_mot = count(texte)
	arbre_huffman = huffmanTree(dictionnaire_de_mot)
	encodeTree(arbre_huffman)
	codage_arbre_huffman = huffmanToCode(arbre_huffman)
	compression = applyCode(codage_arbre_huffman, texte)
	encodage_compression = ByteEncoder([], [])
	encodage_compression.addString(str(compression))
	encodage_compression.write(fichier_ecriture)
	fichier_lecture.close()

# 11
# ...
def HuffmanDecode(fichier_lecture, fichier_ecriture):
	arbre_huffman_fichier = open("encodage_arbre_huffman.txt", 'rb')
	arbre_huffman_string = arbre_huffman_fichier.read()
	pass

if __name__ == '__main__':
	mot = "aababababbabcccbcbccccddddaaaaaaaaaaaaaaaaaaaaaa"
	print(mot)
	dictionnaire_de_mot = count(mot)
	print(dictionnaire_de_mot)
	tas = Tas(lambda x:x[1])
	for valeur in dictionnaire_de_mot:
		tas.ajout(valeur)
	print(tas)

	print(tri_tas(dictionnaire_de_mot, lambda x:x[1]))
	tas.extraire_tout()

	liste_aleatoire = [(randint(1,100), randint(1,100)) for _ in range(10)]
	shuffle(liste_aleatoire)
	print(liste_aleatoire)
	print(tri_tas(liste_aleatoire, lambda x:x[1]))

	arbre_huffman = huffmanTree(dictionnaire_de_mot)
	print("arbre_huffman", arbre_huffman)
	codage_arbre_huffman = huffmanToCode(arbre_huffman)
	print("codage_arbre_huffman", codage_arbre_huffman)

	print(applyCode(codage_arbre_huffman, "baba"))
	print(applyCode(codage_arbre_huffman, mot))

	fichier = open("etranger.txt", 'r')
	texte = fichier.read()
	print(calcul_taux_compression(texte), "%")
	HuffmanEncoding("etranger.txt", "resultat.txt")

	test = ByteEncoder([], [])
	test.addString("Salut, comment ça vas ?\nBien ! ué\n")
	test.write("test.txt")
	for caractere_ascii in test.tableau:
		print(chr(caractere_ascii), end="")

