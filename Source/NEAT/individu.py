# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:40:45 2016

Objet Individu:
    Un objet individu contient un genome et un phenotype, faisant le lien entre
    les deux. Il s'occupera aussi à se muter correctement.

@author: Badr Youbi Idrissi
"""

from genome import Genome
from phenotype import Phenotype
import numpy as np

class Individu():
    
    def __init__(self, nb_entrees, nb_sorties):
        self.nb_e = nb_entrees
        self.nb_s = nb_sorties
        self.genome = Genome(self.nb_e,self.nb_s)
        self.phenotype = Phenotype(self.nb_e,self.nb_s)
        self.idToPos = [(0,i) for i in range(self.nb_e)]
        self.idToPos.extend([(1,j) for j in range(self.nb_s)])
        for c in self.genome.connexions:
            k, l = self.idToPos[c.sortie][1], self.idToPos[c.entree][1]
            self.phenotype.liens[0][1][k,l] = c.poids
    
    def add_node(self, k,l, p1, p2):
        c1, n1 = self.idToPos[k]
        c2, n2 = self.idToPos[l]
        print(c1,n1)
        print(c2,n2)
        if abs(c1-c2) >= 2:
            m = (c1+c2)//2
            p = len(self.phenotype.couches[m])+1
            self.idToPos.append((m, p))
            nc = np.zeros_like
            self.phenotype.couches[m] = np.append(self.phenotype.couches[m],[[0]],1)
            for i in range(len(self.phenotype.couches)):
                if type(self.phenotype.liens[m][i]) != int and type(self.phenotype.liens[i][m]) != int:
                    n1,h1 = self.phenotype.liens[m][i].shape
                    n2,h2 = self.phenotype.liens[i][m].shape
                    self.phenotype.liens[m][i] = np.c_[self.phenotype.liens[m][i], np.zeros((n1,1))]
                    self.phenotype.liens[i][m] = np.r_[self.phenotype.liens[i][m], np.zeros((1, h2+1))]
                else:
                    self.phenotype.liens[m][i] = np.zeros((len(self.phenotype.couches[i]),len(self.phenotype.couches[m])))
                    self.phenotype.liens[m][i] = np.zeros((len(self.phenotype.couches[m]),len(self.phenotype.couches[i])))
                    
            self.phenotype.liens[c1][m][p-1,n1] = p1
            self.phenotype.liens[m][c2][n2,p-1] = p2

        else:
            c = min(c1,c2)
            for i in range(len(self.idToPos)):
                if self.idToPos[i][0] > c:
                    n, h = self.idToPos[i]
                    self.idToPos[i] = (n+1,h)
            c1, n1 = self.idToPos[k]
            c2, n2 = self.idToPos[l]
            for e in self.phenotype.liens:
                e.insert(c+1,0)
            self.phenotype.couches.insert(c+1, np.zeros((1,1)))
            self.phenotype.liens.insert(c+1, [0 for i in range(len(self.phenotype.couches))])
            self.phenotype.liens[c1][c+1] = np.zeros((1,len(self.phenotype.couches[c1])))
            if c1 > 0:
                self.phenotype.liens[c+1][c1] = np.mat(np.zeros((len(self.phenotype.couches[c1]),1)))
                
            self.phenotype.liens[c1][c+1][0,n1] = p1
            if c2 > 0:            
                self.phenotype.liens[c+1][c2] = np.mat(np.zeros((len(self.phenotype.couches[c2]),1)))
                self.phenotype.liens[c+1][c2][n2,0] = p2
                