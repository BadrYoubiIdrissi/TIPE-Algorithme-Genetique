# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:36:14 2016

@author: Badr Youbi Idrissi
"""

from genome import Genome
from phenotype import Phenotype
import pygame
import pygame.gfxdraw
import numpy as np
from pygame.locals import *
      
                           
pygame.init()
screen = pygame.display.set_mode((1000,1000), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60

g = Genome(4, 2, generer = True)

a = Phenotype(2,1)

m01 = np.matrix('1 1; 1 1')
m02 = np.matrix('1 1')
m11 = np.matrix('1 1; 1 1')
m12 = np.matrix('1 1')
m21 = np.matrix('1;1')

a.liens = [[0, m01, m02],
           [0, m11,   m12],
           [0, m21 , 0]]

a.couches = [np.zeros((2,1)), np.zeros((2,1)), np.zeros((1,1))]
             
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            g.weight_mutation()

    a.draw((500,200))
    pygame.display.flip()
