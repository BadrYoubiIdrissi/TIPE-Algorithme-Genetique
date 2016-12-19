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
j = 3
i = Individu(2,1)
c = [Noeud(0,"entree"),Noeud(1,"entree"),Noeud(2,"sortie")]
while True:
    clock.tick()
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            c.append(Noeud(j,"cachee"))
            con = i.genome.connexions[rand.randint(0,len(i.genome.connexions)-1)]
            while not(con.activation):
                con = i.genome.connexions[rand.randint(0,len(i.genome.connexions)-1)]
                print(con)

            d = i.idToPos
            i.add_node(con, 1, 1)
            j+=1
            
    i.phenotype.draw((430,50))
    pygame.display.flip()
    cou = i.phenotype.couches
    lie = i.phenotype.liens
 