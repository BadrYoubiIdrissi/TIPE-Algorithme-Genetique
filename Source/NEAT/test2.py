# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 13:27:03 2017

@author: byoub
"""

from population import Population
import matplotlib.pyplot as plt

ave = [0 for i in range(1000)]
for i in range(10):
    pop = Population(20, 3, 2)
    pop.generer()
    for j in range(1000):
        pop.evoluer()
        ave[j] += (pop.averageFitness)/10

plt.plot(range(1000), ave)
plt.show()
        