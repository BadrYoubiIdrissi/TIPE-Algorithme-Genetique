# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:36:14 2016

@author: Badr Youbi Idrissi
"""

from genome import Genome
import pygame
from pygame.locals import *
      
                           
pygame.init()
screen = pygame.display.set_mode((860,600), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60

g = Genome(4, 2, generer = True)

while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    g.draw(20,20)
    pygame.display.flip()
