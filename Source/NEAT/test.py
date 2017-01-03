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
import utilitaires as ut
import os
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
evol = False

while True:
    clock.tick()
    screen.fill((255,255,255))
    pressed = pygame.key.get_pressed()

    screen.blit(f.render("Fps :"+str(clock.get_fps())[:3],True,(0,0,0)), (0,0))
    screen.blit(f.render("Current generation : " + str(pop.generationCount), True, (0,0,0)), (0,20))
    screen.blit(f.render("Number of species : " + str(len(pop.especes)), True, (0,0,0)), (0,40))
    if pop.generationCount > 0:
        screen.blit(f.render("Best fitness : " + str(pop.best[-1].fitness), True, (0,0,0)), (100,0))
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
                    
                    
        elif event.type == KEYDOWN and event.key == K_SPACE:
            evol = not(evol)
            
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((event.w, event.h), DOUBLEBUF and RESIZABLE)
    if evol:
        pop.evoluer()
    
    pop.draw(f)
    pygame.display.flip()
 
