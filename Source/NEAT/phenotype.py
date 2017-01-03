import numpy as np
import utilitaires as ut
import pygame
import pygame.gfxdraw


class Phenotype(object):
    
    def __repr__(self):
        s=""
        for i in range(len(self.liens)):
            for j in range(1,len(self.liens)):
                s += str((i,j)) + '\n'
                s += self.liens[i][j].__repr__()
                s += '\n\n'
        return s
            
    def __init__(self, nb_entrees, nb_sorties):

        self.nb_entrees = nb_entrees
        self.nb_sorties = nb_sorties
        self.liens = []
        self.couches = []

        self.memoire = False
    
    def generer(self):
        self.liens = [[0, np.mat(np.ones((self.nb_sorties, self.nb_entrees)))],
                      [0, np.mat(np.zeros((self.nb_sorties, self.nb_sorties)))]]
        self.couches= [np.zeros((self.nb_entrees, 1)), np.zeros((self.nb_sorties, 1))]
        
    # Il convient de bien comprendre que la matrice self.liens contient toutes les matrices de transition, qu'elles proviennent ou non d'un lien récurent.
    # Les matrices correspondant à un lien récurrent sous situées sous la diagonale de self.liens
    
    def evaluate(self, e):
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
            self.couches[j] = ut.sigmoide(self.couches[j])
        self.memoire =True
        
    def reinit(self):
        self.memoire = False
        n = len(self.couches)
        for i in range(n):
            self.couches[i] = np.zeros(self.couches[i].shape)
    
    def estComplet(self):
        for i in range(len(self.liens)):
            for j in range(1,len(self.liens)):
                if type(self.liens[i][j]) != int:
                    l,c = self.liens[i][j].shape
                    for k in range(l):
                        for h in range(c):
                            if self.liens[i][j][k,h] == 0:
                                return False
                else:
                    return False
        return True
            
    def insertNode(self, lay):
        longCouche = self.couches[lay].shape[0]
        self.couches[lay] = np.zeros((longCouche+1,1))
        for i in range(len(self.couches)):
            if i == lay:
                if type(self.liens[i][i]) != int:
                    n,h = self.liens[i][i].shape
                    self.liens[i][i] = np.r_[self.liens[i][i], np.zeros((1, h))]
                    self.liens[i][i] = np.c_[self.liens[i][i], np.zeros((n+1, 1))]
                else:
                    self.liens[i][i] = np.mat(np.zeros((len(self.couches[i]),len(self.couches[i]))))
            else:
                if i>0: #On ne touche pas au liens vers les entrees
                    if type(self.liens[lay][i]) != int:
                        n,h = self.liens[lay][i].shape
                        self.liens[lay][i] = np.c_[self.liens[lay][i], np.zeros((n,1))]
                    else:
                        self.liens[lay][i] = np.mat(np.zeros((len(self.couches[i]),len(self.couches[lay]))))
                if type(self.liens[i][lay]) != int:
                    n,h = self.liens[i][lay].shape
                    self.liens[i][lay] = np.r_[self.liens[i][lay], np.zeros((1, h))]
                else:
                    self.liens[i][lay] = np.mat(np.zeros((len(self.couches[lay]),len(self.couches[i]))))
    
    def insertLayer(self, couche):
        #On ajoute une ligne et une colonne de liens
        for e in self.liens:
                e.insert(couche+1,0)
        self.couches.insert(couche+1, np.zeros((0,0)))
        self.liens.insert(couche+1, [0 for i in range(len(self.couches))])
                    
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
                                    if m[k,a] > 0:
                                        color = (50,50,50)
                                    else:
                                        color = (255,0,0)
                                    pygame.draw.aaline(screen, color, posi, posj, True)
                                elif i == j:
                                    if k==a:
                                        pygame.gfxdraw.bezier(screen, [posi,
                                                                       (posi[0]+40,posi[1]),
                                                                       (posi[0],posi[1]+40),
                                                                       posi], 7, (0,0,150))
                                    else:
                                        pygame.gfxdraw.bezier(screen, [posi,
                                                                       ut.offsetMiddle(posi, posj,25),
                                                                       posj], 7, (0,0,150))
                                elif i > j:                          
                                    pygame.gfxdraw.bezier(screen, [posi,
                                                                       ut.offsetMiddle(posi, posj,25),
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

    