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
from connexion import Connexion
from scipy.stats import bernoulli, norm
from temp import entrees

import prob.crossover
import utilitaires as ut
import random as rand

class Individu():
    
    def __init__(self, nb_entrees, nb_sorties, idInd):
        self.nb_e = nb_entrees
        self.nb_s = nb_sorties
        self.id = idInd
        self.espece = None
        self.genome = Genome(self.nb_e,self.nb_s)
        self.phenotype = Phenotype(self.nb_e,self.nb_s)
        self.idToPos = {} #Ce tableau fera l'interface entre le genome et l'individu
        self.fitness = None
        self.sharedFitness = None
    
    def __repr__(self):
        s = "Ind "+str(self.id) + ":"
        s += "\nFitness: "+ str(self.fitness)
        s += "\nShared Fitness: "+ str(self.sharedFitness)
        return s

    
    def generer(self):
        #On ajoute au début les entrées et les sorties
        self.idToPos = { i : (0,i) for i in range(self.nb_e)}
        self.idToPos.update({self.nb_e + j : (1,j) for j in range(self.nb_s)})
        #On met les valeurs de poids de genome dans le phenotype
        self.genome.generer()
        self.phenotype.generer()
        for innov in self.genome.connexions:
            c = self.genome.connexions[innov]
            k, l = self.idToPos[c.sortie][1], self.idToPos[c.entree][1]
            self.phenotype.liens[0][1][k,l] = c.poids
    
    def calculateFitness(self):
        
        self.phenotype.evaluate(entrees[0])
        e1 = self.output()[0][0]
        self.phenotype.evaluate(entrees[1])
        e2 = self.output()[0][0]
        self.phenotype.evaluate(entrees[2])
        e3 = self.output()[0][0]
        self.phenotype.evaluate(entrees[3])
        e4 = self.output()[0][0]

        somErreur = abs(e1) + abs(e2-1.0) + abs(e3 - 1.0) + abs(e4)

        self.fitness = (4-somErreur)**2

        return self.fitness

    def output(self):
        return self.phenotype.couches[-1]
        
    def rawFitness(self):
        if self.fitness == None:
            self.fitness = self.calculateFitness()
        return self.fitness
        
    def add_key(self, nouvid, couche, num):
        """Met à jour la table idToPos en ajoutant un noeud qui 
        sera en la couche et dont le numéro est num"""
        assert nouvid not in self.idToPos, "Le nouvel identifiant ne doit pas être existent"
        self.idToPos[nouvid] = (couche, num)
    
    def insertLayer(self, couche):
        """Insère une couche aprés la couche indiqué en paramètre"""
        #Décale tous les position d'une couche
        for i in self.idToPos:
                if self.idToPos[i][0] > couche:
                    n, h = self.idToPos[i]
                    self.idToPos[i] = (n+1,h)
        #Ajoute une nouvelle couche en inserant de nouvelles matrices liens
        self.phenotype.insertLayer(couche)
    
    def posToId(self, pos):
        for i in self.idToPos:
            if self.idToPos[i] == pos:
                return i
    
    def estRecursive(self, con):
        ce,ne = self.idToPos[con.entree]
        cs,ns = self.idToPos[con.sortie]
        return ce >= cs
                
    def insertNoeudCouche(self, couche, idNouvNoeud):
        assert idNouvNoeud not in self.idToPos, "Noeud déja existant"
        self.phenotype.insertNode(couche)
        self.idToPos[idNouvNoeud] = (couche, len(self.phenotype.couches[couche])-1)
        
    def insertNoeud(self, con, p1, p2, innov, idNouvNoeud):
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
    
        assert c2 - c1 > 0, "Un lien recursif ne peut pas etre coupé"     

        #On a une disjonction de cas selon que les deux noeuds était dans deux couches successifs ou pas
        if c2-c1 >= 2:
            #Si les deux noeuds ne sont pas dans de ux couches succéssifs alors on met le nouveau noeud 
            #dans une couche au milieu des deux couches
            m = (c1+c2)//2
            p = len(self.phenotype.couches[m])  
            #On met à jour la table idToPos
            self.add_key(idNouvNoeud, m,p)
            #On insère le noeud dans la couche m
            self.phenotype.insertNode(m)
            
            self.phenotype.modifierConnexion(idN1,idNouvNoeud, self.idToPos,p1)
            self.phenotype.modifierConnexion(idNouvNoeud, idN2, self.idToPos,p2)
            self.phenotype.modifierConnexion(idN1, idN2, self.idToPos, 0)
            
            self.genome.ajouterConnexion(idN1, idNouvNoeud, p1, innov)
            self.genome.ajouterConnexion(idNouvNoeud, idN2, p2, innov+1)

        elif c2-c1 == 1:
            #On ajoute la nouvelle couche en dessus de la couche en dessous (ie le min)
            c = min(c1,c2)
            
            self.insertLayer(c)
            self.insertNoeudCouche(c+1, idNouvNoeud)
            c1, n1 = self.idToPos[idN1]
            c2, n2 = self.idToPos[idN2]

            self.phenotype.modifierConnexion(idN1, idNouvNoeud, self.idToPos, p1)
            self.phenotype.modifierConnexion(idNouvNoeud, idN2, self.idToPos, p2)
            self.phenotype.modifierConnexion(idN1, idN2, self.idToPos, 0)
            
            self.genome.ajouterConnexion(idN1, idNouvNoeud, p1, innov)
            self.genome.ajouterConnexion(idNouvNoeud, idN2, p2, innov+1)    
            
        self.phenotype.reinit()
    
    def connexionPossible(self):
        if not(self.phenotype.estComplet()):
            tries = 0
            noeuds = self.idToPos.keys()
            noeudsSansEntree = [i for i in noeuds if (i not in range(self.nb_e))]
            e = ut.randomPick(noeuds)
            s = ut.randomPick(noeudsSansEntree)
            c = self.genome.entreeSortieToCon(e,s)
            while tries < 10 and c != None and c.activation:
                e = ut.randomPick(noeuds)
                s = ut.randomPick(noeudsSansEntree)
                c = self.genome.entreeSortieToCon(e,s)
                tries += 1
            if tries < 10:
                if c !=None:
                    return c
                else:
                    return Connexion(e, s, 1)
                
    def mutationPoids(self):
        for i in self.genome.connexions:
            c= self.genome.connexions[i]
            if rand.random() < prob.mutation.poids:
                if rand.random() < prob.mutation.poids_radical:
                    c.poids = 20*rand.random() - 10
                else:
                    c.poids  += 0.5*rand.random()
                self.phenotype.modifierConnexion(c.entree, c.sortie, self.idToPos, c.poids)
                
    def insertLien(self, c, innov):
        self.phenotype.modifierConnexion(c.entree, c.sortie, self.idToPos, c.poids)
        if not(c.activation):
            c.activer()
        else:
            self.genome.ajouter(c, innov)
    
    def draw(self, pos):
        self.phenotype.draw(pos, self.posToId)
    
