# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 11:26:04 2016

@author: Badr Youbi Idrissi
"""

import constants
import utilitaires as ut

class Espece():
    def __init__(self, archetype, espId):
        self.id = espId
        self.leader = archetype
        self.archetype = archetype
        self.contenu = [archetype]
        self.best = [archetype]
        self._bestLastFitness = None
        self.age = 0
        self.stagnationAge = 0
    
    def __repr__(self):
        s = "Individus:"
        for i in self.contenu:
            s += (" " + str(i.id))
        s += "\nBest: "+ str(self.leader.id)
        s += "\nArchetype: "+ str(self.archetype.id)
        return s
        
    def __contains__(self, ind):
        return ind in self.contenu

    def add(self, ind):
        self.contenu.append(ind)
        if ind.rawFitness() > self.leader.rawFitness():
            self.leader = ind
    
    def size(self):
        return len(self.contenu)
    
    def flush(self):
        self.archetype = self.leader
        self._bestLastFitness = self.leader.sharedFitness
        self.contenu = []
        self.age += 1
        
    def bestLastFitness(self):
        assert self._bestLastFitness != None, "Best last fitness not set"
        return self._bestLastFitness
        
    def stagnated(self):
        return self.leader.sharedFitness == self.bestLastFitness()
        
    def averageFitness(self):
        total = 0
        for ind in self.contenu:
            total += ind.sharedFitness
        return total/self.size()
        
    def ajusterFitness(self):
        if self.age > constants.speciation.ageThreshold:
            fitnessModify = constants.speciation.oldFitMod
        else:
            fitnessModify = constants.speciation.youngFitMod
        for ind in self.contenu:
            ind.sharedFitness = ind.rawFitness()*fitnessModify/self.size()
    
    def calculateBest(self):
        self.best = [ind for ind in self.contenu if ind.sharedFitness >= constants.speciation.percentageBest*self.averageFitness()]
        
    def individu(self):
        return ut.randomPick(self.best)
        
    def parents(self):
        return ut.randomCoupleIf(self.best,self.best, lambda a, b: a == b)
          