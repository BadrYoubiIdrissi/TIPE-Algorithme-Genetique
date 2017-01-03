# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

class Connexion(object):
    
    """
    Une connexion relie deux noeuds. Elle a donc comme attributs les identifiants de ces deux noeuds (entrée et sortie).
    Elle est aussi muni d'un poids, le coefficient par lequel est multiplié la valeur donnée en entrée avant 'être envoyée à la sortie.
    Enfin, l'innovation est un chiffre permettant de repérer les connexions selon leur ordre d'apparition
    """
    
    def __init__(self, entree, sortie, poids) :
        
        self.entree = entree
        self.sortie = sortie
        self.poids = poids
        self.activation = True        
    
    def __repr__(self):
        return str(self.entree)+ " -> " + str(self.sortie) + " Actif : " + str(self.activation) + " P : " + str(self.poids) + '\n'
    
    def activer(self):
            self.activation = True
            
    def desactiver(self):
        self.activation = False

        