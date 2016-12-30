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
                           
pygame.init()
screen = pygame.display.set_mode((860, 600), DOUBLEBUF and RESIZABLE)
pygame.display.set_caption("Test")
f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()
nb_e = 3
nb_s = 2

pop = Population(10, nb_e, nb_s)
pop.generer()
ind = Individu(nb_e,nb_s, 3)
while True:
    clock.tick()
    screen.fill((255,255,255))
    pressed = pygame.key.get_pressed()

    screen.blit(f.render("Fps :"+str(clock.get_fps())[:3],True,(0,0,0)), (0,0))
    screen.blit(f.render("Current generation : " + str(pop.generationCount), True, (0,0,0)), (0,20))
    screen.blit(f.render("Number of species : " + str(len(pop.especes)), True, (0,0,0)), (0,40))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            ind = pop.crossover(pop.contenu[0], pop.contenu[1])
            print(pop.distance(pop.contenu[0], pop.contenu[1]))
        elif event.type == KEYDOWN and event.key == K_DOWN:
            pop.evoluer()
            os.system('cls')
            for e in pop.especes:
                print(e)
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((event.w, event.h), DOUBLEBUF and RESIZABLE)
    if pressed[K_SPACE]:
        pop.evoluer()
    
    pop.evaluate(np.ones((3,1)))
    pop.draw()
    ind.genome.draw((50,300))
    pygame.display.flip()
 
