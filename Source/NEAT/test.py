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
                           
pygame.init()
screen = pygame.display.set_mode((1000, 800), DOUBLEBUF)
pygame.display.set_caption("Test")
f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
clock = pygame.time.Clock()
nb_e = 3
nb_s = 2

pop = Population(2, nb_e, nb_s)
pop.generer()

while True:
    clock.tick()
    screen.fill((255,255,255))
    pressed = pygame.key.get_pressed()

    screen.blit(f.render(str(clock.get_fps())[:3],True,(0,0,0)), (0,0))
    screen.blit(f.render("Current generation : " + str(pop.generationCount), True, (0,0,0)), (0,20))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            for i in pop.contenu:
                print(i.genome.connexions)
                
    if pressed[K_SPACE]:
        pop.evoluer()
    if pressed[K_n]:
        pass


    pop.draw()
    pygame.display.flip()
 
