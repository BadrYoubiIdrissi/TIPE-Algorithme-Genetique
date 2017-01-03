# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
"""

from genome2 import Genome2
from noeud import Noeud
from connexion import Connexion
import random as rd
from utilitaires import elimine_doubl_int
from utilitaires import elimine_doubl_co

class Population():
    
    def __init__(self, length):
        self.length = length
        self.contenu = []
        self.noeuds = []
        self.generationCount = 0
        self.indiceInnovation = 0
        
    def genrand(self, max, nb_entr, nb_sort):
        for i in range (self.length):
            self.contenu.append(Genome2([nb_entr, nb_sort], 'generer'))
        
            
    def fusionrand(self, ind1, ind2):
        f1 = self.fitness(ind1)
        f2 = self.fitness(ind2)
        
        entr = ind1.nb_entree
        sort = ind1.nb_sortie #tous les individus ont les mêmes listes d'entrées et de sorties
        
        co1 = sorted(ind1.connexions, key = lambda connexion : connexion.innovation)
        co2 = sorted(ind2.connexions, key = lambda connexion : connexion.innovation)
        n1 = len(co1)
        n2 = len(co2)
        i1 = 0
        i2 = 0
        
        lc = [] #Cette liste contient toutes les connexions du fils
        ln = [] #Cette liste contient tous les noeuds du fils
        
        while i1 < n1 and i2 < n2 :
            if co1[i1].innovation == co2[i2].innovation :
                if not(co1[i1].activation) or not(co2[i2].activation) :
                    if rd.random() < 0.5 :
                        lc.append(co1[i1])
                        ln.append(co1[i1].entree)
                        ln.append(co1[i1].sortie)
                    else : 
                        lc.append(co2[i2])
                        ln.append(co2[i2].entree)
                        ln.append(co2[i2].sortie)
                else :
                    if rd.random() < 0.5 :
                        lc.append(co1[i1])
                        ln.append(co1[i1].entree)
                        ln.append(co1[i1].sortie)
                    else :
                        lc.append(co2[i2])
                        ln.append(co2[i2].entree)
                        ln.append(co2[i2].sortie)
                i1 += 1
                i2 += 1
            else :
                if co1[i1].innovation > co2[i2].innovation :
                    if f2 > f1 :
                        lc.append(co2[i2])
                        ln.append(co2[i2].entree)
                        ln.append(co2[i2].sortie)
                    i2 += 1
                else :
                    if f1 > f2 :
                        lc.append(co1[i1])
                        ln.append(co1[i1].entree)
                        ln.append(co1[i1].sortie)
                    i1 += 1
        if i1 < n1 and f1 > f2 :
            while i1 < n1:
                lc.append(co1[i1])
                ln.append(co1[i1].entree)
                ln.append(co1[i1].sortie)
                i1 += 1
        if i2 < n2 and f2 > f1 :
            while i2 < n2:
                lc.append(co2[i2])
                ln.append(co2[i2].entree)
                ln.append(co2[i2].sortie)
                i2 += 1      
            
        #On connait toutes les connexions, ainsi que tous les noeuds impliqués.
        #Cependant il y a des doublons dans la liste des noeuds
        #Pour les enlever, tri puis suppression
        
        l2 = elimine_doubl_int(ln)
        ln_fin = []
                
        for i in l2:
            ln_fin.append(Noeud(i, "cache"))
        
        print(entr)
        print(sort)
        print(len(l2))
        
        fils = Genome2(entr, sort, len(l2), elimine_doubl_co(lc))
        return fils 
        
    def fitness(self, ind):
        f = rd.random()
        print("fitness est")
        print(f)
        print()
        return f
