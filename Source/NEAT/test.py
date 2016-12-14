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
                           
pygame.init()
screen = pygame.display.set_mode((860 ,600), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60

i = Individu(4,2)

while True:
    clock.tick()
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            i.add_node(0,4, 1, 1)
        
    i.phenotype.eval(np.sin(pygame.time.get_ticks()*np.ones((4,1))/1000))
    i.phenotype.draw((500,200))
    pygame.display.flip()
