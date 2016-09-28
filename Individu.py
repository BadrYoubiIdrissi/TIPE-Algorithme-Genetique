# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:59:47 2016

@author: Profs&Eleves
"""
from Connexion import Connexion
from Gene import Gene


class Individu(object) :
    
    """
    Un individu est constitué d'un nombre d'entrées, non nul, et d'un contenu.
    Son contenu est l'ensemble de ses gènes et des connexions entre ces gènes.
    """
    
    def __init__(self, nb_entree, nb_sortie):
        self.nb_entree = nb_entree
        l_entrees = []
        for i in (nb_entree):
            l_entrees.append(Gene(i, "entree"))
        self.entrees = l_entrees
        
        l_sorties = []
        for i in (nb_sortie):
            l_sorties.append(Gene(nb_entree + i, "sortie"))
        self.sorties = l_sorties
        
        l_connexions = []
        for i in (nb_entree):
            for j in (nb_sortie):
                l_connexions.append(Connexion(i,j,1.0,0))
        self.connexions = l_connexions
                
        
            
        
            