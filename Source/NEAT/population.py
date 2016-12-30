# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
"""

from individu import Individu
from noeud import Noeud
from espece import Espece
from scipy.stats import bernoulli, norm
from numpy import inf, floor
from copy import deepcopy
from copy import copy

import prob.mutation
import constants.speciation
import utilitaires as ut
import pygame
import random as rand

class Population():
    
    def __init__(self, length, nb_e, nb_s):
        self.length = length
        self.contenu = [Individu(nb_e,nb_s, i) for i in range(length)]
        self.oldGen = []
        self.nb_e = nb_e
        self.nb_s = nb_s
        self.noeuds = [Noeud(i, "entree") for i in range(nb_e)]
        self.noeuds.extend([Noeud(i,"sortie") for i in range(nb_e, nb_e + nb_s)])
        self.generationCount = 0
        self.indiceInnovation = 0
        self.lastIndId = length
        self.lasEspId = 0
        self.historique = []
        self.especes = []
        """Cette liste contiendra les différentes opérations génétiques structurelles
        ce qui nous évitera d'avoir une explosion d'indice d'innovations
        ce tableau contiendra des triplet (type, id noeud entree, id noeud sortie)
        type prendra les valeurs 0 si l'opération était une mutation de lien
        et 1 si c'est une mutation de noeud"""
    
    def tournamentSelection(self, liste, nbCandidates=None, probBest=0.8):
        
        if nbCandidates == None:
            nbCandidates = rand.randint(1, self.length)
        candidates = rand.sample(liste, nbCandidates)
        return ut.bestIndividual(candidates)
        
    def crossover(self, ind1, ind2):
        fils = Individu(self.nb_e, self.nb_s, self.lastIndId)
        self.lastIndId += 1
        #On fait le croisement des genomes dans un premier temps
        plusGrdInnov = max(max(ind1.genome.connexions), max(ind2.genome.connexions))
        plusFort = ind1.sharedFitness > ind2.sharedFitness 
        if plusFort:
            champ = deepcopy(ind1)
        else:
            champ = deepcopy(ind2)
        fils.phenotype = champ.phenotype
        fils.idToPos = champ.idToPos
        
        for i in range(plusGrdInnov+1):
            ind1con = ind1.genome.connexions.get(i, None)
            ind2con = ind2.genome.connexions.get(i, None)
            if ind1con == None and ind2con == None:
                pass
            elif ind1con != None and ind2con != None:
                c = copy(ut.randomPick([ind1con, ind2con]))
                #Ici on dans le cadre de deux connexions de meme indice d'innov
                if not(ind1con.activation) or not(ind2con.activation) : 
                    #On a une probabilité "prob.crossover.activation" d'activer
                    #les connexions désactivés dans les parents
                    if bernoulli.rvs(prob.crossover.activation):
                        c.activer()
                    else : 
                        c.desactiver()
                        
                fils.genome.connexions[i] = c
                fils.phenotype.modifierConnexion(c.entree, c.sortie, champ.idToPos, c.poids)
            #Les cas ici traitent les genes disjoints ou en excès
            elif ind1con == None:
                if not(plusFort):
                    fils.genome.connexions[i] = ind2con
                    fils.phenotype.modifierConnexion(ind2con.entree, ind2con.sortie, ind2.idToPos, ind2con.poids)
            elif ind2con == None:
                if plusFort:
                    fils.genome.connexions[i] = ind1con
                    fils.phenotype.modifierConnexion(ind1con.entree, ind1con.sortie, ind1.idToPos, ind1con.poids)

        fils.phenotype.reinit()
        return fils
        
    def generer(self):
        for ind in self.contenu:
            ind.generer()
            
        for i in range(self.nb_e):
            for j in range(self.nb_e, self.nb_e + self.nb_s):
                self.historique.append((0,i,j))
                self.indiceInnovation += 1
    
    def mutationConnexion(self, ind):
        con = ind.connexionPossible()
        if con != None:
            con.poids = norm.rvs()
            for i in range(len(self.historique)):
                if self.historique[i] == (0,con.entree,con.sortie):
                    ind.insertLien(con, i)
                    break
            else:
                ind.insertLien(con, self.indiceInnovation)
                self.historique.append((0,con.entree, con.sortie))
                self.indiceInnovation += 1
    
    def mutationNoeud(self, ind):
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
  
    def evoluer(self):
        """Cette fonction evoluera la population à la génération suivante
            Les étapes suivantes sont faites:
                1-On commence par supprimer tous les individus des éspèces sauf le meilleur
                2-On sépare la population en espèces
                3-On vide le contenu et on garde la dérnière génération
                4-On reproduit les espèces"""
        #Etape 1:

        #Etape 2:
        for i in self.contenu:
            i.calculateFitness()
        for e in self.especes:
            e.ajusterFitness()
            e.calculateBest()
        #Etape 3

        if self.generationCount>0:
            self.oldGen = self.contenu   #Attention: J'essaye d'éviter les deepcopy donc oldGen peut changer
            self.contenu = []
            aveFit = ut.average([ind.sharedFitness for ind in self.oldGen])
            indivAl = self.tournamentSelection(self.oldGen)
        else:
            aveFit = ut.average([ind.rawFitness() for ind in self.contenu])
            indivAl = ut.randomPick(self.contenu)

        #Etape 4
        for e in self.especes:
            tailleProgeniture = int(floor(self.length*e.averageFitness()/aveFit))

            for i in range(tailleProgeniture):
                if len(self.contenu) < self.length:
                    if i == 0:
                        enfant = deepcopy(e.leader)
                    elif len(e.best) > 1:
                        par1, par2 = e.parents()
                        enfant = self.crossover(par1, par2)
                    else:
                        enfant = deepcopy(e.individu())
                        enfant.id = self.lastIndId
                        self.lastIndId += 1
                        
                    enfant.mutationPoids()
                    if bernoulli.rvs(prob.mutation.connexion):
                        self.mutationConnexion(enfant)
                    
                    if bernoulli.rvs(prob.mutation.noeud):
                        self.mutationNoeud(enfant)

                    self.contenu.append(enfant)
            e.lastBestFitness = e.leader.sharedFitness
                    
        assert self.length - len(self.contenu) <= 1, "La population est morte"
        if self.length - len(self.contenu) == 1:
            self.contenu.append(indivAl)
        
        for i in range(len(self.especes)):
            if e.age > 1:
                e = self.especes[i]
                if e.stagnated():
                    e.stagnationAge += 1
                else:
                    e.stagnationAge = 0
                if e.stagnationAge >= constants.speciation.stagnationAgeThresh:
                    del self.especes[i]
        for e in self.especes:
            e.flush()
        self.updateEspeces()
        self.generationCount += 1
            
        
    def updateEspeces(self):
        for ind in ut.shuffle(self.contenu):
            i = 0
            while i < len(self.especes):
                if self.distance(ind, self.especes[i].archetype) <= constants.speciation.distThreshold:
                    self.especes[i].add(ind)
                    ind.espece = i
                    break
                i += 1
            if i == len(self.especes):
                self.especes.append(Espece(deepcopy(ind), self.lasEspId))
                self.lasEspId += 1
        i = 0
        while i < len(self.especes):
            if self.especes[i].contenu == []:
                del self.especes[i]
            else:
                for ind in self.especes[i].contenu:
                    ind.espece = i
                i +=1
            
    def distance(self, ind1, ind2):
        innovind1 = max(ind1.genome.connexions)
        innovind2 = max(ind2.genome.connexions)
        plusGrdInnov = max(innovind1, innovind2)
        E = 0
        D = 0
        W = 0
        nshared = 0
        for i in range(plusGrdInnov+1):
            ind1con = ind1.genome.connexions.get(i, None)
            ind2con = ind2.genome.connexions.get(i, None)
            if ind1con != None and ind2con != None:
                W += abs(ind1con.poids - ind2con.poids)
                nshared += 1
            elif (ind1con == None or ind2con == None):
                if i <= min(innovind1, innovind2):
                    D += 1
                else:
                    E += 1
        
        c1 = constants.speciation.coExcess
        c2 = constants.speciation.coDisjoint
        c3 = constants.speciation.coWeights
        if self.length >= 20:   N = self.length
        else: N = 1
#        print("Excess :", E)
#        print("Disjoint :", D)
#        print("Average weight diff :", W/nshared)
#        print("Shared :", nshared)
        if nshared == 0:
            return inf
        else:
            return (c1*E + c2*D)/N + c3*W/nshared

    def evaluate(self, e):
        for ind in self.contenu:
            ind.phenotype.evaluate(e)
    
    def findEspeces(self, ind):
        for e in self.especes:
            if ind in e:
                return e.id
            
    def draw(self):
        n = ut.carrePlusProche(self.length)
        k = 0
        screen = pygame.display.get_surface()
        f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        width, height = screen.get_size()
        xstep, ystep = (width/n), (height/n)
        for i in range(n):
            for j in range(n):
                if k < len(self.contenu):
                    ind = self.contenu[k]
                    tesp = f.render("Espece: " + str(self.findEspeces(ind)), True, (0,0,0))
                    screen.blit(tesp,\
                                (int(j*xstep+ xstep/2 - tesp.get_width()/2) ,70+ int(i*ystep)))
                    ind.draw((int(j*xstep+ xstep/2) ,70 + int(i*ystep + 40)))
                    k += 1
            
