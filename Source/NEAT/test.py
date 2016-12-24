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
import utilitaires as ut
                           
pygame.init()
screen = pygame.display.set_mode((1000, 1000), DOUBLEBUF)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
FPS = 60
nb_e = 3
nb_s = 2
j = nb_e + nb_s
k = 0
innov = nb_e * nb_s
ind = Individu(nb_e,nb_s)
ind.generer()
#historique = {i+j : (0,i,j) for i in range(nb_e) for j in range(nb_e,nb_e+nb_s)}
historique = {}
indGen = Individu(nb_e,nb_s)
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
            con = ut.randomPick(list(ind.genome.connexions.values()))
            ind.insert_noeud(con, 1, 1, innov, j)
            historique[innov] = (1,con.entree,j)
            historique[innov+1] = (1,j,con.sortie)
            j += 1
            innov += 2
#            ind.add_key(5, 1, 2)
#            ind.phenotype.insertNode(1)
#            print(ind.phenotype)
        elif event.type == KEYDOWN and event.key == K_n:
#            for k in historique:
#                print(historique[k])
            indGen.phenotype.insertLayer(k-1)
            k+=1
        elif event.type == KEYDOWN and event.key == K_UP:
            pass
#            indGen.phenotype.insertNode(k-1)
#            indGen.phenotype.evaluate(np.ones((len(genpheno.couches[0]),1)))
#            print(genpheno)

    if pressed[pygame.K_DOWN]:
        c = ind.insert_lien_al(1, innov)
        if c != None:   
            e,s = c
            historique[innov] = (0,e,s)
            innov += 1
    
            
    ind.phenotype.draw((200,50), ind.posToId)
    indGen.phenotype.draw((200, 500))
    ind.genome.draw((350, 50))
    ind.phenotype.evaluate(np.ones((3,1)))
    pygame.display.flip()
 