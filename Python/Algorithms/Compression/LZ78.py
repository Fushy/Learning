from huffman import *
import os
import decimal
from random import choice

def lz78(texte, taille=None):
	dictionnaire = {'' : 0}
	pile = ''
	sequence = []
	curseur = 1
	for lettre in texte:
		if pile + lettre not in dictionnaire:
			sequence.append((dictionnaire[pile], lettre))
			if taille is not None and curseur >= taille:
				dictionnaire = {'' : 0}
				curseur = 1
			dictionnaire[pile + lettre] = curseur
			pile = ''
			curseur += 1
		else:
			pile += lettre
	if pile != '':
		sequence.append((dictionnaire[pile[:-1]], pile[-1]))
	return sequence

def un_lz78(sequence, taille=None):
	dictionnaire = {}
	mot = ""
	for (index, caractere) in sequence:
		if index not in dictionnaire:
			if taille is not None and len(dictionnaire) + 1 >= taille:
				dictionnaire = {}
			mot += caractere
			dictionnaire[len(dictionnaire) + 1] = caractere
		else :
			tmp = dictionnaire[index] + caractere
			mot += tmp
			if taille is not None and len(dictionnaire) + 1 >= taille:
				dictionnaire = {}
			dictionnaire[len(dictionnaire) + 1] = tmp
	return mot

def algorithme_LZ78_est_ok(mot=None):
	if mot is not None:
		if un_lz78(lz78(mot)) != mot:
			print("False :", mot, "\n", lz78(mot), un_lz78(lz78(mot)))
			return False
		if un_lz78(lz78(mot, 4), 4) != mot:
			print("False :", mot, "\n", lz78(mot, 4), un_lz78(lz78(mot, 4), 4))
			return False
		return True
	for _ in range(100):
		u = "".join([choice(['a', 'b', 'c']) for _ in range(10)])
		if un_lz78(lz78(u)) != u:
			print("False :", u, "\n", lz78(u), un_lz78(lz78(u)))
			return False
		if un_lz78(lz78(u, 4), 4) != u:
			print("False :", u, "\n", lz78(u, 4), un_lz78(lz78(u, 4)))
			return False
	return True

# print(algorithme_LZ78_est_ok())

fichier = open("etranger.txt", "r")
etranger_txt = fichier.read()
decimal.Decimal(2)
# print(algorithme_LZ78_est_ok(etranger_txt))

liste_lz78 =  lz78(etranger_txt)
# Nous devons tranformer la liste en texte
texte_lz78 = "".join([str(u) + v for (u,v) in liste_lz78]) # Si cette méthode est incorrecte dû à la perte d'information ((clé, valeur) => qui est la clé qui est la valeur), on cherche alors un caractère unique n'appartenant pas au texte afin de le mettre avant et après une clé pour pouvoir différencier les clés des valeurs.
taille_etranger_txt = os.path.getsize("etranger.txt") * 8
print("La taille initiale du fichier etranger.txt est de", taille_etranger_txt, "bits.")
taille_huffman_etranger_txt = huffmanSize(texte_lz78)
print("La taille de la compression du résultat de lz78 par Huffman est de", taille_huffman_etranger_txt, "bits.")
print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_etranger_txt / taille_etranger_txt * 100, prec=2))

indices = "".join([str(indice) for (indice, caractere) in liste_lz78])
caracteres = "".join([caractere for (indice, caractere) in liste_lz78])
taille_huffman_indicesCaractres_etranger_txt = huffmanSize(indices) + huffmanSize(caracteres)
print("La taille du fichier compressé si on appliquait cette technique à etranger.txt est de", taille_huffman_indicesCaractres_etranger_txt, "bits.")
print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_indicesCaractres_etranger_txt / taille_etranger_txt * 100, prec=2))

liste_lz78 =  lz78(etranger_txt, 2048)
indices = "".join([str(indice) for (indice, caractere) in liste_lz78])
caracteres = "".join([caractere for (indice, caractere) in liste_lz78])
taille_huffman_indicesCaractres_etranger_txt = huffmanSize(indices) + huffmanSize(caracteres)
print("La taille du fichier compressé si on appliquait cette technique à etranger.txt est de", taille_huffman_indicesCaractres_etranger_txt, "bits.")
print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_indicesCaractres_etranger_txt / taille_etranger_txt * 100, prec=2))
