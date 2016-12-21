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
    def __init__(self, nb_entrees, nb_sorties, generer = True):
        self.nb_entree = nb_entrees            
        self.nb_sortie = nb_sorties
        self.connexions = []
        if generer:
            indInnov = 0
            for i in range(self.nb_entree):
                for j in range(self.nb_entree, self.nb_entree + self.nb_sortie):
                    self.connexions.append(Connexion(i,j,1,indInnov))
                    indInnov += 1
            
    """ L'evaluation est maintenant faite dans le phenotype
     def eval_part(self, numero, val_entree):
        \"""
        Cette fonction est une fonction intermédiaire récursive qui évalue la valeur à la sortie de n'importre quel noeud, en prenant comme argument une liste de valeurs, une par entrée
        Cette fonction utilise des principes de programmation dynamique : une foisque la valeur en un noeud est calculée, on la stocke dans l'attributvaleur
        \"""
        
        assert len(val_entree) == self.nb_entree
        
        if numero < self.nb_entree :
            return val_entree[numero]
            
        else :  
            l =[]
            for i in self.connexions :
                if i.sortie == numero:
                    for j in self.noeuds :
                         if j.id == i.entree :
                            l.append([i,j])
            som = 0
            for k in l:
                i= k[0]
                j=k[1]
                
                if j.valeur == None :
                    j.valeur = self.eval_part(j.id, val_entree)
                
                print((i.poids)*(j.valeur))
                som = som + (i.poids)*(j.valeur)
            
            return (1/(1+exp(-som)))
        
    
    def evaluation(self, val_entree):
        \"""
        Cettefonction utilise la fonction eval intermédiaire, appliquée en chacun desgènes de sortie.
        On réinitialise au début de chaque calcul les valeurs des noeuds pour éviter des restes de calculs précédents
        \"""
        
        for i in self.noeuds:
            if i.fonction != "entree":
                i.valeur = None
        
        l_sorties= []
        for j in self.sort:
            l_sorties.append(self.eval_part(j.id, val_entree))
            
        return l_sorties"""
            
    def weight_mutation(self):
        for c in self.connexions:
            if bernoulli.rvs(prob.mutation.poids_radical):
                c.poids = norm.rvs()
            else:
                c.poids  += 0.1*norm.rvs()
    
    """ La mutation est maintenant principalement faite dans l'individu
    def node_mutation(self):
        connex_alea = random.sample(self.connexions,1)[0]
        connex_alea.activation = False
        
        noeud = Noeud(len(self.noeuds)+1, "cache")
        entree = connex_alea.entree
        sortie = connex_alea.sortie
        
        self.indiceInnov += 1
        con1 = Connexion(entree, noeud.id, norm.rvs(), self.indiceInnov)
        
        self.indiceInnov += 1
        con2 = Connexion(noeud.id, sortie, norm.rvs(), self.indiceInnov)
        
        self.noeuds.append(noeud)
        self.connexions.append(con1)
        self.connexions.append(con2)
        
        x1,y1 = self.nodePos[entree]
        x2,y2 = self.nodePos[sortie]
        
        self.nodePos[noeud.id] = (int((x1+x2)/2),int((y1+y2)/2))
    
    def connection_mutation(self):
        entree = random.randint(0,len(self.noeuds)-1)
        sortie = random.randint(entree+1, len(self.noeuds)-1)
        self.indiceInnov += 1
        self.connexions.append(Connexion(entree, sortie, norm.rvs(), self.indiceInnov))
    """
    def ajouterConnexion(self, entree, sortie, poids, innov):
        self.connexions.append(Connexion(entree,sortie,poids,innov))
    
    def innovToCon(self, innov):
        for c in self.connexions:
            if c.innovation == innov:
                return c
    
    def connexionExiste(self,e,s):
        return ((e,s) in [(c.entree,c.sortie) for c in self.connexions if c.activation])
    
    def draw(self, pos):
        x, y = pos
        screen = pygame.display.get_surface()
        fon = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        for i in range(len(self.connexions)):
            c = self.connexions[i]
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+60*i, y, 60, 40), 3)
            t = fon.render(str(c.entree)+" -> "+str(c.sortie), True, (0,0,0))
            tinnov = fon.render(str(c.innovation), True, (0,0,0))
            screen.blit(t,(x+60*i+13, y+20))
            screen.blit(tinnov, (x+60*i+25, y+7))
            
            
            
            