# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:37:05 2016

@author: Physique
"""

from population import Population
from genome2 import Genome2
from connexion import Connexion

pop = Population(0)

thelma =  Genome2(3,2,6,[Connexion(0,3,1,1), Connexion(1,3,1,2), Connexion(2,5,1,5), Connexion(5,4,1,6)])
print(thelma.connexions)
print()
louise = Genome2(3,2,5,[Connexion(0,3,1,1), Connexion(1,3,1,2), Connexion(2,3,1,4), Connexion(2,4,1,3)])
print(louise.connexions)
print()

xiv = pop.fusionrand(thelma, louise)
print(xiv.connexions)
print(xiv.noeuds)

