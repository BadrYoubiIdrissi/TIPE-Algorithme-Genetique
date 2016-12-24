# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
"""

from individu import Individu
from noeud import Noeud
from scipy.stats import bernoulli, norm

import random as rd
import prob.mutation
import utilitaires as ut
import pygame


class Population():
    
    def __init__(self, length, nb_e, nb_s):
        self.length = length
        self.contenu = [Individu(nb_e,nb_s) for i in range(length)]
        self.nb_e = nb_e
        self.nb_s = nb_s
        self.noeuds = [Noeud(i, "entree") for i in range(nb_e)]
        self.noeuds.extend([Noeud(i,"sortie") for i in range(nb_e, nb_e + nb_s)])
        self.generationCount = 0
        self.indiceInnovation = 0
        self.historique = [] 
        """Cette liste contiendra les différentes opérations génétiques structurelles
        ce qui nous évitera d'avoir une explosion d'indice d'innovations
        ce tableau contiendra des triplet (type, id noeud entree, id noeud sortie)
        type prendra les valeurs 0 si l'opération était une mutation de lien
        et 1 si c'est une mutation de noeud"""
    
    def generer(self):
        for ind in self.contenu:
            ind.generer()
            
        for i in range(self.nb_e):
            for j in range(self.nb_e, self.nb_e + self.nb_s):
                self.historique.append((0,i,j))
                self.indiceInnovation += 1
    
    def evoluer(self):
        """Cette fonction evoluera la population à la génération suivante"""
        #Pour le moment on évolue juste en faisant les différente mutations
        self.generationCount += 1
        for ind in self.contenu:
            ind.mutationPoids()
            if rd.random() <= prob.mutation.connexion:
                con = ind.connexionPossible()
                con = norm.rvs()
                if con != None:
                    for i in range(len(self.historique)):
                        if self.historique[i] == (0,con.entree,con.sortie):
                            ind.insertLien(con, i)
                            break
                    else:
                        ind.insertLien(con, self.indiceInnovation)
                        self.historique.append((0,con.entree, con.sortie))
                        self.indiceInnovation += 1
                        
            if rd.random() <= prob.mutation.noeud:
                con = ut.randomPick(list(ind.genome.connexions.values()))
                idNouvNoeud = len(self.noeuds)
                for i in range(self.indiceInnovation):
                    t1, e1, s1 = self.historique[i]
                    if t1 == 1:
                        t2, e2, s2 = self.historique[i+1]
                        if e1 == con.entree and s2 == con.sortie and (s1 not in ind.idToPos):
                            ind.insertNoeud(con, 1, con.poids, i, s1)
                            break
                else:
                    ind.insertNoeud(con, 1, con.poids, self.indiceInnovation, idNouvNoeud)
                    self.historique.append((1,con.entree,idNouvNoeud))
                    self.historique.append((2,idNouvNoeud,con.sortie))
                    self.noeuds.append(Noeud(idNouvNoeud, "cachee"))
                    self.indiceInnovation += 2
        
        
        
        
    def draw(self):
        n = ut.carrePlusProche(self.length)
        k = 0
        screen = pygame.display.get_surface()
        width, height = screen.get_size()
        xstep, ystep = (width/n), (height/n)
        for i in range(n):
            for j in range(n):
                if k < len(self.contenu):
                    ind = self.contenu[k]
                    ind.draw((int(j*xstep+ xstep/2) , int(i*ystep + 10)))
                    k += 1
            
