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
        self.indiceInnovation += 1
    
    def mutation_lien():
        pass
    
    def evoluer(self):
        self.generationCount += 1
            
    def fusionrand(self, ind1, ind2):
        f1 = fitness(ind1)
        f2 = fitness(ind2)
        
        entr = ind1.entrees
        sort = ind1.sorties #tous les individus ont les mêmes listes d'entrées et de sorties
        
        lc = [] #Cette liste contient toutes les connexions du fils
        ln = [] #Cette liste contient tous les noeuds du fils
        for i in ind1.connexions:
            for j in ind2.connexions:
                if i.innovation == j.innovation :
                    if not(i.activation) or not(j.activation) :
                        if rd.random() < 0.5 :
                            lc.append(i)
                            ln.append(i.entree)
                            ln.append(i.sortie)
                        else : 
                            lc.append(j)
                            ln.append(j.entree)
                            ln.append(j.sortie)
                    if rd.random() < 0.5 :
                        lc.append(i)
                        ln.append(i.entree)
                        ln.append(i.sortie)
                    else :
                        lc.append(j)
                        ln.append(j.entree)
                        ln.append(j.sortie)
                else:
                    if f1>f2:
                        if rd.random() < 0.5 :
                            lc.append(i)
                            ln.append(i.entree)
                            ln.append(i.sortie)
                    else :
                        if rd.random() < 0.5 :
                            lc.append(j)
                            ln.append(j.entree)
                            ln.append(j.sortie)
        #On connait toutes les connexions, ainsi que tous les noeuds impliqués.
        #Cependant il y a des doublons dans la liste des noeuds
        #Pour les enlever, tri puis suppression
        ln2 = sorted(ln, key=lambda noeud: noeud.id)
        n = len(ln2)
        doublons = []
        for i in range (n-1):
            if ln2(i) == ln(i+1):
                doublons.append(i)
        for i in doublons :
            ln2.remove(i)
        
        fils = Genome(entr, sort, ln2)
        return fils 
        
        
        
