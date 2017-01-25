# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:47:29 2016

@author: Thomas Guilmeau
    def __init__(self, length, nb_e, nb_s):
        self.length = length
"""

from individu import Individu
from noeud import Noeud
from espece import Espece
from numpy import inf, floor
from numpy.random import rand as randMat
from copy import deepcopy
from copy import copy

import prob.mutation
import constants.speciation
import utilitaires as ut
import pygame
import random as rand
import matplotlib.pyplot as plt

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
        self.lastEspId = 0
        self.averageFitness = None
        self.historique = []
        self.especes = []
        self.histEspeces = []
        self.bestDisplay = 1
        self.best = []
#        self.especesFig, self.especesAx = plt.subplots(figsize=(20, 20*500/860))
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
                    if rand.random() < prob.crossover.activation:
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
            if rand.random() < prob.mutation.recursif:
                i = 0
                while not(ind.estRecursive(con)) and i < 10:
                    con = ind.connexionPossible()
                    if con == None:
                        return None
                    i += 1
            else:
                i = 0
                while ind.estRecursive(con) and i < 10 :
                    con = ind.connexionPossible()
                    if con == None:
                        return None
                    i += 1
            if i < 10:
                con.poids = 30*rand.random() - 15
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
        while ind.estRecursive(con):
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

        if self.generationCount>0:
            indivAl = self.tournamentSelection(self.contenu)
            self.contenu = []
        else:
            indivAl = ut.randomPick(self.contenu)

        for e in self.especes:
            tailleProgeniture = int(1 + floor(self.length*e.averageRawFitness()/self.averageFitness))

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
                    if rand.random() < prob.mutation.connexion:
                        self.mutationConnexion(enfant)
                    
                    if rand.random() < prob.mutation.noeud:
                        self.mutationNoeud(enfant)

                    self.contenu.append(enfant)
            e.lastBestFitness = e.leader.fitness
                    
        assert self.length - len(self.contenu) <= 1, "La population est morte"
        if self.length - len(self.contenu) == 1:
            self.contenu.append(deepcopy(indivAl))
        
#        for i in range(len(self.especes)):
#            if e.age > 1:
#                e = self.especes[i]
#                if e.stagnated():
#                    e.stagnationAge += 1
#                else:
#                    e.stagnationAge = 0
#                if e.stagnationAge >= constants.speciation.stagnationAgeThresh:
#                    del self.especes[i]
        
        for e in self.especes:
            e.flush()
            
        self.updateEspeces()
#        if len(self.especes) > constants.speciation.nbSpeciesTarget:
#            constants.speciation.distThreshold += constants.speciation.distanceThresholdMod
#        elif len(self.especes) < constants.speciation.nbSpeciesTarget:
#            constants.speciation.distThreshold -= constants.speciation.distanceThresholdMod
        for i in self.contenu:
            i.calculateFitness()
            i.phenotype.reinit()
        for e in self.especes:
            e.ajusterFitness()
            e.calculateBest()
        
#        self.updateBest()
        self.updateAverageFitness()
        self.generationCount += 1
    
    def updateAverageFitness(self):
        self.averageFitness = ut.average([ind.fitness for ind in self.contenu])
        
    def updateEspeces(self):
        for ind in ut.shuffle(self.contenu):
            i = 0
            while i < len(self.especes):
                if self.distance(ind, self.especes[i].archetype) <= constants.speciation.distThreshold:
                    self.especes[i].add(ind)
                    break
                i += 1
            if i == len(self.especes):
                nouvE = Espece(ind, self.lastEspId, self.generationCount)
                self.especes.append(nouvE)
#                self.histEspeces.append((randMat(1,3),lambda:nouvE.evolPrcnt))
                self.lastEspId += 1
        i = 0
        while i < len(self.especes):
            if self.especes[i].contenu == []:
                del self.especes[i]
            else:
                i +=1
        
        for e in self.especes:
            e.evolPrcnt.append(e.size()*100/self.length)


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
        N = self.length
#        print("Excess :", E)
#        print("Disjoint :", D)
#        print("Average weight diff :", W/nshared)
#        print("Shared :", nshared)
        if nshared == 0:
            return inf
        else:
            return (c1*E + c2*D)/N + c3*W/nshared
    
    def updateBest(self):
        for i in self.contenu:
            i.calculateFitness()
        self.best = sorted(self.contenu, key = lambda ind: ind.fitness)[self.length-self.bestDisplay:]
    
    def evaluate(self, e):
        for ind in self.contenu:
            ind.phenotype.evaluate(e)
    
    def findEspeces(self, ind):
        for e in self.especes:
            if ind in e:
                return e.id
    
    def getBestFitness(self):
        if self.best != []:
            return self.best[-1].fitness, self.best[-1].sharedFitness
    
    def getBestSharedFitness(self):
        mx = 0
        for i in self.contenu:
            if i.sharedFitness != None and i.sharedFitness >= mx:
                mx = i.sharedFitness
        return mx
                
    def draw(self, f):
        n = ut.carrePlusProche(self.bestDisplay)
        k = 0
        screen = pygame.display.get_surface()
        width, height = screen.get_size()
        xstep, ystep = (width/n), (height/n)
        
        l = [0 for _ in range(self.generationCount)]
        
        for e in self.histEspeces:
            for i in range(len(l)):
                l[i] = l[i] + e[1]()[i]
            self.especesAx.fill_between(range(self.generationCount),0, l, color = e[0])
        
#        self.especesFig.canvas.draw()
#        size = self.especesFig.get_size_inches()*self.especesFig.dpi
#        f = pygame.image.fromstring(self.especesFig.canvas.tostring_argb() , size.astype(int) , 'ARGB', False)
##        f = pygame.transform.scale(f, (width, 300))
#        screen.blit(f, (0,height-500))
        
        for i in range(n):
            for j in range(n):
                if k < len(self.best):
                    ind = self.best[k]
#                    tesp = f.render("Espece: " + str(self.findEspeces(ind)), True, (0,0,0))
#                    screen.blit(tesp,\
#                                (int(j*xstep+ xstep/2 - tesp.get_width()/2) ,70+ int(i*ystep)))
                    ind.draw((int(j*xstep+ xstep/2) ,70 + int(i*ystep + 40)))
                    k += 1
            
