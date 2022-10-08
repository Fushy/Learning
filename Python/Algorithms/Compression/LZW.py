import copy
from huffman import *
import os
import decimal
from random import choice

def lzw(mot, dictionnaire_taille=256):
	dictionnaire = {chr(i): i for i in range(dictionnaire_taille)}
	string = ""
	sequence = []
	for lettre in mot:
		pile = string + lettre
		if pile in dictionnaire:
			string = pile
		else:
			sequence.append(dictionnaire[string])
			if len(dictionnaire) <= dictionnaire_taille:
				dictionnaire[pile] = dictionnaire_taille
				dictionnaire_taille += 1
			string = lettre
		if string in dictionnaire:
			sequence.append(dictionnaire[string])
	return sequence

def un_lzw(sequence, size=256):
	dictionnaire = {i:chr(i) for i in range(size)}
	mot = dictionnaire[sequence[0]]
	string = chr(sequence[0])
	for code in sequence[1:]:
		if code not in dictionnaire:
			dictionnaire[code] = string + string[0]
		mot += dictionnaire[code]
		if len(string) != 0:
			dictionnaire[size] = string + dictionnaire[code][0]
			size += 1
		string = dictionnaire[code]
	return mot

def algorithme_LZW_est_ok(mot=None):
	if mot is not None:
		if un_lzw(lzw(mot)) != mot:
			print("False :", mot, "\n", lzw(mot), un_lzw(lzw(mot)))
			return False
		# if un_lzw(lzw(mot, 4), 4) != mot:
		# 	print("False :", mot, "\n", lzw(mot, 4), un_lzw(lzw(mot, 4) 4))
		# 	return False
		return True
	for _ in range(100):
		u = "".join([choice(['a', 'b', 'c']) for _ in range(10)])
		if un_lzw(lzw(u)) != u:
			print("False :", u, "\n", lzw(u), un_lzw(lzw(u)))
			return False
		# if un_lzw(lzw(u, 4), 4) != u:
		# 	print("False :", u, "\n", lzw(u, 4), un_lzw(lzw(u, 4)))
		# 	return False
	return True

print(algorithme_LZW_est_ok())

# fichier = open("etranger.txt", "r")
# etranger_txt = fichier.read()
# decimal.Decimal(2)
# print(algorithme_LZW_est_ok(etranger_txt))

# liste_lzw =  lzw(etranger_txt)
# # Nous devons tranformer la liste en texte
# texte_lzw = "".join([str(u) + v for (u,v) in liste_lzw]) # Si cette méthode est incorrecte dû à la perte d'information ((clé, valeur) => qui est la clé qui est la valeur), on cherche alors un caractère unique n'appartenant pas au texte afin de le mettre avant et après une clé pour pouvoir différencier les clés des valeurs.
# taille_etranger_txt = os.path.getsize("etranger.txt") * 8
# print("La taille initiale du fichier etranger.txt est de", taille_etranger_txt, "bits.")
# taille_huffman_etranger_txt = huffmanSize(texte_lzw)
# print("La taille de la compression du résultat de lzw par Huffman est de", taille_huffman_etranger_txt, "bits.")
# print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_etranger_txt / taille_etranger_txt * 100, prec=2))
#
# indices = "".join([str(indice) for (indice, caractere) in liste_lzw])
# caracteres = "".join([caractere for (indice, caractere) in liste_lzw])
# taille_huffman_indicesCaractres_etranger_txt = huffmanSize(indices) + huffmanSize(caracteres)
# print("La taille du fichier compressé si on appliquait cette technique à etranger.txt est de", taille_huffman_indicesCaractres_etranger_txt, "bits.")
# print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_indicesCaractres_etranger_txt / taille_etranger_txt * 100, prec=2))
#
# liste_lzw =  lzw(etranger_txt, 2048)
# indices = "".join([str(indice) for (indice, caractere) in liste_lzw])
# caracteres = "".join([caractere for (indice, caractere) in liste_lzw])
# taille_huffman_indicesCaractres_etranger_txt = huffmanSize(indices) + huffmanSize(caracteres)
# print("La taille du fichier compressé si on appliquait cette technique à etranger.txt est de", taille_huffman_indicesCaractres_etranger_txt, "bits.")
# print("L'amélioration est de {:.{prec}f}%".format(100 - taille_huffman_indicesCaractres_etranger_txt / taille_etranger_txt * 100, prec=2))
