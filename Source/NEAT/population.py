# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
"""

from individu import Individu
from Noeud import Noeud
import random as rd
import prob.mutation
import utilitaires as ut

class Population():
    
    def __init__(self, length, nb_e, nb_s):
        self.length = length
        self.contenu = [Individu(nb_e,nb_s)]
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
        
        for i in range(nb_e):
            for j in range(nb_e,nb_e+nb_s):
                self.historique.append((0,i,j))
                self.indiceInnovation += 1
                                
    def evoluer(self):
        """Cette fonction evoluera la population à la génération suivante"""
        #Pour le moment on évolue juste en faisant les différente mutations
        for ind in self.contenu:
            r = rd.random()
            if r <= prob.mutation.connexion:
                con = ind.connexionPossible()
                for i in range(len(self.historique)):
                    if self.historique[i] == (0,con.entree,con.sortie):
                        ind.insertLien(con, i)
                        break
                else:
                    ind.insertLien(con, self.indiceInnovation)
                    self.historique[self.indiceInnovation] = (0,con.entree, con.sortie)
                    self.indiceInnovation += 1
                        
            elif r <= prob.mutation.connexion + prob.mutation.noeuds:
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
                    self.historique[self.indiceInnovation] = (1,con.entree,idNouvNoeud)
                    self.historique[self.indiceInnovation+1] = (1,idNouvNoeud,con.sortie)
                    self.noeuds.append(Noeud(idNouvNoeud, "cachee"))
                    self.indiceInnovation += 2
            else:
                pass
            
        
        
        
