# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: eleve
"""

from genome import Genome
from Noeud import Noeud
from Connexion import Connexion
import random as rd

class Population():
    
    def __init__(self, length):
        assert (length <=0)
        self.length = length
        self.contenu = []
        self.generationCount = 0
        
    def genrand(self, max, nb_entr, nb_sort):
        for i in range (self.length):
            self.contenu.append(genome([nb_entr, nb_sort], 'generer'))
            
    def fusionrand(self, ind1, ind2):
        f1 = fitness(ind1)
        f2 = fitness(ind2)
        l = []
        for i in ind1.connexions:
            for j in ind2.connexions:
                if i.innovation == j.innovation :
                    if not(i.activation) or not(j.activation) :
                        if rd.random() < 0.5 :
                            l.append(i)
                        else : 
                            l.append(j)
                    if rd.random() < 0.5 :
                        l.append(i)
                    else :
                        l.append(j)
                else:
                    if f1>f2:
                        l.append(i)
                        
        