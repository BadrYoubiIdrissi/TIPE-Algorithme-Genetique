# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 12:21:44 2016

@author: Badr Youbi Idrissi

Un genome est un contennaire de connexions

C'est sur cet objet que va opérer les opérateurs génétiques
"""

import prob.mutation
from scipy.stats import bernoulli, norm
from connexion import Connexion
import pygame

class Genome():
    def __init__(self, nb_entrees, nb_sorties):
        self.nb_entree = nb_entrees            
        self.nb_sortie = nb_sorties
        self.connexions = {}
    
    def generer(self):
        indInnov = 0
        for i in range(self.nb_entree):
            for j in range(self.nb_entree, self.nb_entree + self.nb_sortie):
                self.connexions[indInnov] = Connexion(i,j,1)
                indInnov += 1
            
    def weight_mutation(self):
        for c in self.connexions:
            if bernoulli.rvs(prob.mutation.poids_radical):
                c.poids = norm.rvs()
            else:
                c.poids  += 0.1*norm.rvs()
    
    def ajouterConnexion(self, entree, sortie, poids,  innov):
        assert innov not in self.connexions, "Ce numero d'innovation est déja attribué : " + str(innov) + " Connexion :" + str(Connexion(entree,sortie,poids)) 
        self.connexions[innov] = Connexion(entree,sortie,poids)
    
    def ajouter(self, c, innov):
        assert innov not in self.connexions, "Ce numero d'innovation est déja attribué : " + str(innov) + " Connexion :" + str(Connexion(entree,sortie,poids)) 
        self.connexions[innov] = c
        
    def entreeSortieToCon(self,e,s):
        for innov in self.connexions:
            c = self.connexions[innov]
            if c.entree == e and c.sortie == s:
                return c
        else:
            return None
    
    def draw(self, pos):
        x, y = pos
        screen = pygame.display.get_surface()
        fon = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        i = 0
        for innov in self.connexions:
            c = self.connexions[innov]
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+60*i, y, 60, 40), 3)
            if c.activation:
                color = (0,0,0)
            else:
                color = (255,0,0)
            t = fon.render(str(c.entree)+" -> "+str(c.sortie), True, color)
            tinnov = fon.render(str(innov), True, (0,0,0))
            screen.blit(t,(x+60*i+13, y+20))
            screen.blit(tinnov, (x+60*i+25, y+7))
            i+=1
            
            
            
            