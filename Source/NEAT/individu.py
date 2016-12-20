# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:40:45 2016

Objet Individu:
    Un objet individu contient un genome et un phenotype, faisant le lien entre
    les deux. Il s'occupera aussi à se muter correctement.

@author: Badr Youbi Idrissi
"""

from genome import Genome
from phenotype import Phenotype
import numpy as np
import random as rand

class Individu():
    
    def __init__(self, nb_entrees, nb_sorties):
        self.nb_e = nb_entrees
        self.nb_s = nb_sorties
        self.genome = Genome(self.nb_e,self.nb_s)
        self.phenotype = Phenotype(self.nb_e,self.nb_s)
        #On initialise ici la table idToPos qui fera le lien entre le genome et le phenotype
        #On ajoute au début les entrées et les sorties
        self.idToPos = [(0,i) for i in range(self.nb_e)]
        self.idToPos.extend([(1,j) for j in range(self.nb_s)])
        #On met les valeurs de poids de genome dans le phenotype
        for c in self.genome.connexions:
            k, l = self.idToPos[c.sortie][1], self.idToPos[c.entree][1]
            self.phenotype.liens[0][1][k,l] = c.poids
    
    def add_key(self, couche, num):
        """Met à jour la table idToPos en ajoutant un noeud qui 
        sera en la couche et dont le numéro est num"""
        self.idToPos.append((couche, num))
    
    def insert_layer(self, couche):
        """Insère une couche aprés la couche indiqué en paramètre"""
        #Décale tous les position d'une couche
        for i in range(len(self.idToPos)):
                if self.idToPos[i][0] > couche:
                    n, h = self.idToPos[i]
                    self.idToPos[i] = (n+1,h)
        #Ajoute une nouvelle couche en inserant de nouvelles matrices liens
        #On ajoute une ligne et une colonne de liens
        for e in self.phenotype.liens:
                e.insert(couche+1,0)
        self.phenotype.couches.insert(couche+1, np.zeros((1,1)))
        self.phenotype.liens.insert(couche+1, [0 for i in range(len(self.phenotype.couches))])
    
    def posToId(self, pos):
        for i in range(len(self.idToPos)):
            if self.idToPos[i] == pos:
                return i
        
    def insert_noeud(self, con, p1, p2, innov):
        """Cette fonction prend une connexion déja existante et la remplace par deux
           nouvelle connexions et un noeud intermédiaire qui occupera la couche milieu si elle existe
           et créera une nouvelle couche si la connexion relie deux couches succéssives ou la même couche"""
        #On désactive la connexion précèdente
        idN1 = con.entree
        idN2 = con.sortie
        con.desactiver()
        #On récupère la position dans le phénotype des deux noeuds précèdemment reliés
        c1, n1 = self.idToPos[idN1]
        c2, n2 = self.idToPos[idN2]
        #Le nouveau noeud aura le prochain identifiant disponible
        idNouvNoeud = len(self.idToPos)
        
        #On a une disjonction de cas selon que les deux noeuds était dans deux couches successifs ou pas
        if abs(c1-c2) >= 2:
            #Si les deux noeuds ne sont pas dans de ux couches succéssifs alors on met le nouveau noeud 
            #dans une couche au milieu des deux couches
            m = (c1+c2)//2
            p = len(self.phenotype.couches[m])  
            #On met à jour la table idToPos
            self.add_key(m,p)
            #On insère le noeud dans la couche m
            self.phenotype.insertNode(m)
            
            self.phenotype.modifierConnexion(idN1,idNouvNoeud, self.idToPos,p1)
            self.phenotype.modifierConnexion(idNouvNoeud, idN2, self.idToPos,p2)
            self.phenotype.modifierConnexion(idN1, idN2, self.idToPos, 0)
            
            self.genome.ajouterConnexion(idN1, idNouvNoeud, p1, innov)
            self.genome.ajouterConnexion(idNouvNoeud, idN2, p2, innov+1)

        else:
            #On ajoute la nouvelle couche en dessus de la couche en dessous (ie le min)
            c = min(c1,c2)
            
            self.insert_layer(c)
            self.add_key(c+1, 0)
            c1, n1 = self.idToPos[idN1]
            c2, n2 = self.idToPos[idN2]

            self.phenotype.modifierConnexion(idN1, idNouvNoeud, self.idToPos, p1)
            self.phenotype.modifierConnexion(idNouvNoeud, idN2, self.idToPos, p2)
            self.phenotype.modifierConnexion(idN1, idN2, self.idToPos, 0)
            
            self.genome.ajouterConnexion(idN1, idNouvNoeud, p1, innov)
            self.genome.ajouterConnexion(idNouvNoeud, idN2, p2, innov+1)
        
        self.phenotype.reinit()
    
    def insert_lien_al(self, poids, innov):
        e = rand.randint(0, len(self.idToPos)-1)
        s = rand.randint(self.nb_e, len(self.idToPos)-1)
        self.phenotype.modifierConnexion(e, s, self.idToPos, poids)
        self.genome.ajouterConnexion(e,s,poids,innov)