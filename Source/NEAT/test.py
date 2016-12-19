# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:36:14 2016

@author: Badr Youbi Idrissi
"""

import pygame
import pygame.gfxdraw
import numpy as np
from pygame.locals import *
import random as rand
from individu import Individu
from noeud import Noeud
                           
pygame.init()
screen = pygame.display.set_mode((860 ,600), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60
nb_e = 3
nb_s = 2
j = nb_e + 1
i = Individu(nb_e,nb_s)

while True:
    clock.tick()
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            pass
            
    i.phenotype.draw((430,50), i.posToId)
    pygame.display.flip()
    i.phenotype.eval(np.ones((nb_e,1)))
 