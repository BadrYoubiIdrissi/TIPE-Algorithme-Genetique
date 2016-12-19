import numpy as np
from math import exp
from utilitaires import *
import pygame
import pygame.gfxdraw


class Phenotype(object):
    
    def __repr__(self):
        a=self.liens[:,1:]
        s=""
        for l in a:
            for c in l:
                s += c.__repr__()
                s += '\t'
            s += '\n\n'
        return s
            
    def __init__(self, nb_entrees, nb_sorties):

        self.nb_entrees = nb_entrees
        self.nb_sorties = nb_sorties
        
        self.liens = [[0, np.mat(np.ones((nb_sorties, nb_entrees)))],
                      [0, np.mat(np.zeros((nb_sorties, nb_sorties)))]]
        self.couches= [np.zeros((nb_entrees, 1)), np.zeros((nb_sorties, 1))]
                       
        self.noeuds = []
        
        self.memoire = False
    
    # Il convient de bien comprendre que la matrice self.liens contient toutes les matrices de transition, qu'elles proviennent ou non d'un lien récurent.
    # Les matrices correspondant à un lien récurrent sous situées sous la diagonale de self.liens
    
    def eval(self, e):
        # assert len(e) == self.nb_entrees
        n = len(self.couches)
        self.couches[0] = e
        for j in range(1,n): #Oncalcule la couches numero j
            c=np.zeros(self.couches[j].shape) #Cette liste vacontenir les valeurs provenant de l'instant d'avant, pour ne pasmodifier les couches existantes
            for i in range(j,n): #On calcule les éléments provenant de liens récursifs, à l'instant précédent.
                if type(self.liens[i][j]) != int:
                    c += self.liens[i][j]*self.couches[i]
                    
            for i in range(j): #on calcule leséléments du même instant, qui vienne du dessous de l'arbre
                if type(self.liens[i][j]) != int:
                    c += self.liens[i][j]*self.couches[i]
                
            self.couches[j] = c
            self.couches[j] = sigmoide(self.couches[j])
        self.memoire =True
        
    def reinit(self):
        self.memoire = False
        n = len(self.couches)
        for i in range(n):
            self.couches[i] = np.zeros(self.couches[i].shape)
            
    def insertNode(self, lay):
        self.couches[lay] = np.append(self.couches[lay],[[0]],0)
        for i in range(len(self.couches)):
            if i>0:
                if type(self.liens[lay][i]) != int:
                    n,h = self.liens[lay][i].shape
                    self.liens[lay][i] = np.c_[self.liens[lay][i], np.zeros((n,1))]
                else:
                    self.liens[lay][i] = np.mat(np.zeros((len(self.couches[i]),len(self.couches[lay]))))
            if type(self.liens[i][lay]) != int and i != lay:
                n,h = self.liens[i][lay].shape
                self.liens[i][lay] = np.r_[self.liens[i][lay], np.zeros((1, h))]
            else:
                self.liens[i][lay] = np.mat(np.zeros((len(self.couches[lay]),len(self.couches[i]))))
    
    def modifierConnexion(self, k,l, idToPos,poids):
        c1, n1 = idToPos[k]
        c2, n2 = idToPos[l]
        assert c2>0, "Ne peut pas faire de lien vers une entrée"
        if type(self.liens[c1][c2]) != int:
            self.liens[c1][c2][n2,n1] = poids
        else:
            nb_s = len(self.couches[c2])
            nb_e = len(self.couches[c1])
            self.liens[c1][c2] = np.mat(np.zeros((nb_s,nb_e)))
            self.liens[c1][c2][n2,n1] = poids

    def posToCoord(self, posnn, spos, offsetx = 50, offsety = 30):
        i, j = posnn
        x, y = spos
        return (int(x - (len(self.couches[i])/2 - j)*offsetx),int(y+ offsetx*i))
    
        
    def draw(self, pos, posToId = None):
        x,y = pos
        screen = pygame.display.get_surface()
        f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        for i in range(len(self.couches)):
            for j in range(len(self.couches)):
                m = self.liens[i][j]
                if type(m) != int:
                    sizei, sizej  = m.shape
                    for k in range(sizei):
                        for a in range(sizej):
                            if m[k,a] != 0:
                                posi, posj = self.posToCoord((i,a), pos), self.posToCoord((j,k), pos)
                                if i < j:
                                    pygame.draw.aaline(screen, (50,50,50), posi, posj, True)
                                elif i == j:
                                    if k==a:
                                        pygame.gfxdraw.bezier(screen, [posi,
                                                                       (posi[0]+40,posi[1]),
                                                                       (posi[0],posi[1]+40),
                                                                       posi], 7, (0,0,150))
                                    else:
                                        pygame.gfxdraw.bezier(screen, [posi,
                                                                       offsetMiddle(posi, posj,25),
                                                                       posj], 7, (0,0,150))
                                elif i > j:                          
                                    pygame.gfxdraw.bezier(screen, [posi,
                                                                       offsetMiddle(posi, posj,25),
                                                                       posj], 7, (0,0,150))
        for i in range(len(self.couches)):
            l = len(self.couches[i])
            for j in range(l):
                x, y = self.posToCoord((i,j), pos)
                color = (66, 134, 244)
                pygame.gfxdraw.aacircle(screen, x, y, 10, color)
                t = f.render(str(self.couches[i][j][0])[:4], True, (0,0,0))
                screen.blit(t, (x+20,y-5))
                pygame.gfxdraw.filled_circle(screen, x, y, 10, color)
                if posToId != None :
                    tid = f.render(str(posToId((i,j))), True, (0,0,0))
                    screen.blit(tid, (x-4,y-5))
            
                
#a = phenotype(2,1)
#
#m01 = np.matrix('1 0')
#m02 = np.matrix('0 0.01')
#m12 = np.matrix('0.0001')
#m21 = np.matrix('0.5')
#
#a.liens = [[0, m01, m02],
#           [0, 0,   m12],
#           [0, m21 , 0]]
#
#a.couches = [np.zeros((3,1)), np.zeros((1,1)), np.zeros((1,1))]


        
    