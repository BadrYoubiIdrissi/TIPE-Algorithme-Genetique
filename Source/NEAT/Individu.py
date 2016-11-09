# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:59:47 2016

@author: Profs&Eleves
"""
from connexion import Connexion
from Noeud import Noeud
from math import exp
from copy import copy


class Individu(object) :
    
    """
    Un individu est constitué d'un nombre d'entrées, non nul, et d'un contenu.
    Son contenu est l'ensemble de ses gènes et des connexions entre ces gènes.
    Les gènes sont contenus dans trois listes: la liste des gènes d'entrée, celle des gènes de sortie, et celle des gènes intermédiaires, qui contient aussi ceux de sortie
    En effet, ceux-ci sont dans un certian sens intermédiaires car ils nécessitent le calcul des gènes précédents pour trouver leurvaleur
    """
    
    def __init__(self, nb_entree, nb_sortie):
        self.nb_entree = nb_entree
        l_entrees = []
        for i in range(nb_entree):
            l_entrees.append(Noeud(i, "entree"))
        self.entrees = l_entrees
        
        l_sorties = []
        for i in range(nb_sortie):
            l_sorties.append(Noeud(nb_entree + i, "sortie"))
        self.sorties = l_sorties
        
        l_noeuds = []
        for i in self.sorties :
            l_noeuds.append(i)
        self.noeuds = l_noeuds
        
        l_connexions = []
        for i in range(nb_entree):
            for j in range (nb_sortie):
                l_connexions.append(Connexion(i,j,1,0))
        self.connexions = l_connexions
                
    #Reflechir au numéro d'innovation ?    
    
    def eval_part(self, numero, val_entree):
        """
        Cette fonction est une fonction intermédiaire récursive qui évalue la valeur à la sortie de n'importre quel noeud, en prenant comme argument une liste de valeurs, une par entrée
        Cette fonction utilise des principes de programmation dynamique : une foisque la valeur en un noeud est calculée, on la stocke dans l'attributvaleur
        """
        
        assert len(val_entree) == self.nb_entree
        
        if numero < self.nb_entree :
            return val_entree[numero]
            
        else :  
            l =[]
            for i in self.connexions :
                for j in self.noeuds :
                    if i.sortie == numero and j.id == i.entree :
                        l.append([i,j])
            sum = 0
            for k in l:
                i= k[0]
                j=k[1]
                
                if j.valeur == None :
                    j.valeur = self.eval_part(j.id, val_entree)
                    
                sum = sum + (i.poids)*(j.valeur)
            
            return (1/(1+exp(-sum)), sum)
        
    
    def evaluation(self, val_entree):
        """
        Cettefonction utilise la fonction eval intermédiaire, appliquée en chacun desgènes de sortie.
        On réinitialise au début de chaque calcul les valeurs des noeuds pour éviter des restes de calculs précédents
        """
        
        for i in self.noeuds:
            i.valeur = None
        
        l_sorties= []
        for j in self.sorties :
            l_sorties.append(self.eval_part(j.id, val_entree))
            
        return l_sorties
                
                    
        

        
        
            
        
            
