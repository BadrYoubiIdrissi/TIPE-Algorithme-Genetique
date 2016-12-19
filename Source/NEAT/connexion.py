# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

class Connexion(object):
    
    """
    Une connexion relie deux gènes. Elle a donc comme attributs les identifiants de ces deux gènes (entrée et sortie).
    Elle est aussi muni d'un poids, le coefficient par lequel est multiplié la valeur donnée en entrée avant 'être envoyée à la sortie.
    Enfin, l'innovation est un chiffre permettant de repérer les gènes selon leur ordre d'apparition
    """
    
    def __init__(self, entree, sortie, poids, innovation) :
        
        self.entree = entree
        self.sortie = sortie
        self.poids = poids
        self.innovation = innovation
        self.activation = True
        
    
    def __repr__(self):
        return "Entree : " + str(self.entree)+ " Sortie : " + str(self.sortie) + '\n'

    def desactiver(self):
        self.activation = False
