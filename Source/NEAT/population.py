# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
"""

from genome import Genome
from individu import Individu
from Noeud import Noeud
from Connexion import Connexion
import random as rd

class Population():
    
    def __init__(self, length, nb_e, nb_s):
        self.length = length
        self.contenu = [Individu(nb_e,nb_s)]
        self.nb_e = nb_e
        self.nb_s = nb_s
        self.noeuds = [Noeud(i, "entree") for i in range(nb_e)]
        self.noeuds.extend([Noeud(i,"sortie") for i in range(nb_e, nb_e + nb_s)])
        self.generationCount = 0
        self.indiceInnovation = nb_e*nb_s
    
    def mutation_noeud(self, idIndiv):
        self.noeuds.append(Noeud(len(self.noeuds), "cachee")) #To be continued
        con = None
        p1 = None
        p2 = None
        self.contenu[idIndiv].insert_noeud(con, p1, p2, self.indiceInnovation+1)
        self.indiceInnovation += 2
    
    def mutation_lien():
        pass
    
    def evoluer(self):
        self.generationCount += 1
            
        
        
        
