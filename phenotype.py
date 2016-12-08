import numpy as np
from math import exp


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
        
        self.liens = [[0, np.ones((nb_sorties, nb_entrees))],
                      [0, np.zeros((nb_sorties, nb_entrees))]]
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
                c += self.liens[i][j]*self.couches[i]
               
            for i in range(j): #on calcule leséléments du même instant, qui vienne du dessous de l'arbre
                c += self.liens[i][j]*self.couches[i]
                
                
            self.couches[j] = c #On somme les deux contributions
            self.couches[j] = sigmoide(self.couches[j])
        self.memoire =True
        
    def reinit(self):
        self.memoire = False
        n = len(self.couches)
        for i in range(n):
            self.couches[i] = np.zeros(self.couches[i].shape)
            
    

def sigmoide(vect):
    return (1/(1+np.exp(-vect)))
    
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


        
    