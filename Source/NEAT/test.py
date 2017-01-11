# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:36:14 2016

@author: Badr Youbi Idrissi
"""

import pygame
import pygame.gfxdraw
import numpy as np
from pygame.locals import *
from individu import Individu
from phenotype import Phenotype
from population import Population
from datadisplay import DataDisplay
import utilitaires as ut
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
                           
pygame.init()
screen = pygame.display.set_mode((860, 600), DOUBLEBUF and RESIZABLE)
pygame.display.set_caption("Test")
f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()
nb_e = 3
nb_s = 1

pop = Population(50, nb_e, nb_s)
pop.generer()

status = DataDisplay((0,0), padding = 20)
status.add("FPS", lambda : clock.get_fps())
status.add("Current generation", lambda : pop.generationCount)
status.add("Number of species", lambda : len(pop.especes))
status.add("Best fitness", pop.getBestFitness)
status.add("Best shared fitness", pop.getBestSharedFitness)

evol = False

while True:
    clock.tick()
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            nbPoints = 50
            X,Y = np.meshgrid(np.linspace(0,1,nbPoints),np.linspace(0,1,nbPoints))
            Z = np.zeros((nbPoints,nbPoints))
            for i in range(nbPoints):
                for j in range(nbPoints):
                    pop.best[-1].phenotype.evaluate(ut.entree('1;'+str(X[i,j])+';'+str(Y[i,j])))
                    Z[i,j] = pop.best[-1].output()
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            surf = ax.plot_surface(X, Y, Z)
            plt.show()
        
        elif event.type == KEYDOWN and event.key == K_DOWN:
            l = [pop.contenu[i].fitness for i in range(pop.length)]
            l2 = [pop.contenu[i].sharedFitness for i in range(pop.length)]
            plt.plot(range(pop.length), l)
            plt.plot(range(pop.length), l2)
            plt.show()
                 
        elif event.type == KEYDOWN and event.key == K_e:
            evol = not(evol)
            
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((event.w, event.h), DOUBLEBUF and RESIZABLE)

        
    if evol:
        pop.evoluer()
        if (pop.generationCount % 10 == 0):
            pop.updateBest()
            
    
    pop.draw(status.police)
    status.draw()
    pygame.display.flip()
            
 
