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
import utilitaires as ut
                           
pygame.init()
screen = pygame.display.set_mode((1000 ,1000), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60
nb_e = 3
nb_s = 2
j = nb_e+ nb_s + 1
i = Individu(nb_e,nb_s)

while True:
    clock.tick()
    screen.fill((255,255,255))
    pressed = pygame.key.get_pressed()
    f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    screen.blit(f.render(str(clock.get_fps())[:3],True,(0,0,0)), (0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            con = ut.randomPick(i.genome.connexions)
            i.insert_noeud(con, 1, 1, 0, j)
            j += 1
#            i.add_key(5, 1, 2)
#            i.phenotype.insertNode(1)
#            print(i.phenotype)
    if pressed[pygame.K_DOWN]:
        i.insert_lien_al(1, 0)
    
            
    i.phenotype.draw((200,50), i.posToId)
    pygame.display.flip()
    i.phenotype.eval(np.ones((nb_e,1)))
    ut.checkCoherence(i)
 