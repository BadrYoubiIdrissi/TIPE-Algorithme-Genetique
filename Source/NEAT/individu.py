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
import prob.crossover
import utilitaires as ut

class Individu():
    
    def __init__(self, nb_entrees, nb_sorties, generer = True):
        self.nb_e = nb_entrees
        self.nb_s = nb_sorties
        self.genome = Genome(self.nb_e,self.nb_s, generer)
        self.phenotype = Phenotype(self.nb_e,self.nb_s, generer)
        
        if generer:
            #On initialise ici la table idToPos qui fera le lien entre le genome et le phenotype
            #On ajoute au début les entrées et les sorties
            self.idToPos = { i : (0,i) for i in range(self.nb_e)}
            self.idToPos.update({self.nb_e + j : (1,j) for j in range(self.nb_s)})
            #On met les valeurs de poids de genome dans le phenotype
            for c in self.genome.connexions:
                k, l = self.idToPos[c.sortie][1], self.idToPos[c.entree][1]
                self.phenotype.liens[0][1][k,l] = c.poids
        else:
            self.idToPos = {}
        
    
    def __add__(self, mate):
        fils = Individu(self.nb_e, self.nb_s, generer = False)
        
        #On fait le croisement des genomes dans un premier temps
        plusGrdInnov = max(self.genome.connexions[-1].innovation, mate.genome.connexions[-1].innovation)
        plusFort = self.fitness() > mate.fitness()
        egal = self.fitness() == mate.fitness()
        plusFaible = not(plusFort) and not(egal)
        for i in range(plusGrdInnov+1):
            selfcon = self.genome.innovToCon(i)
            matecon = self.genome.innovToCon(i)
            if selfcon != None and matecon != None:
                c = ut.randomPick([selfcon, matecon])
                #Ici on dans le cadre de deux connexions de meme indice d'innov
                if not(i.activation) or not(j.activation) : 
                    #On a une probabilité "prob.crossover.activation" d'activer
                    #les connexions désactivés dans les parents
                    if rand.random() < prob.crossover.activation :
                        c.activer()
                    else : 
                        c.desactiver()
                fils.genome.connexions.append(c)
            #Les cas ici traitent les genes disjoints ou en excès
            elif selfcon == None:
                if egal and rand.random() <= 0.5:
                    fils.genome.connexions.append(matecon)
                elif plusFaible:
                    fils.genome.connexions.append(matecon)
            elif matecon == None:
                if plusFort:
                    fils.genome.connexions.append(selfcon)
                elif egal and rand.random() <= 0.5:
                        fils.genome.connexions.append(selfcon)
        
        #Puis le croisement des phenotypes
        
        return fils
        
    def fitness(self):
        return 0
        
    def add_key(self, nouvid, couche, num):
        """Met à jour la table idToPos en ajoutant un noeud qui 
        sera en la couche et dont le numéro est num"""
        assert nouvid not in self.idToPos, "Le nouvel identifiant ne doit pas être existent"
        self.idToPos[nouvid] = (couche, num)
    
    def insert_layer(self, couche):
        """Insère une couche aprés la couche indiqué en paramètre"""
        #Décale tous les position d'une couche
        for i in self.idToPos:
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
        for i in self.idToPos:
            if self.idToPos[i] == pos:
                return i
        
    def insert_noeud(self, con, p1, p2, innov, idNouvNoeud):
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
        
        #On a une disjonction de cas selon que les deux noeuds était dans deux couches successifs ou pas
        if abs(c1-c2) >= 2:
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

        else:
            #On ajoute la nouvelle couche en dessus de la couche en dessous (ie le min)
            c = min(c1,c2)
            
            self.insert_layer(c)
            self.add_key(idNouvNoeud,c+1, 0)
            c1, n1 = self.idToPos[idN1]
            c2, n2 = self.idToPos[idN2]

            self.phenotype.modifierConnexion(idN1, idNouvNoeud, self.idToPos, p1)
            self.phenotype.modifierConnexion(idNouvNoeud, idN2, self.idToPos, p2)
            self.phenotype.modifierConnexion(idN1, idN2, self.idToPos, 0)
            
            self.genome.ajouterConnexion(idN1, idNouvNoeud, p1, innov)
            self.genome.ajouterConnexion(idNouvNoeud, idN2, p2, innov+1)
        
        self.phenotype.reinit()
    
    def insert_lien_al(self, poids, innov):
        if not(self.phenotype.estComplet()):
            noeuds = self.idToPos.keys()
            noeudsSansEntree = [i for i in noeuds if (i not in range(self.nb_e))]
            e = ut.randomPick(noeuds)
            s = ut.randomPick(noeudsSansEntree)
            c = self.genome.entreeSortieToCon(e,s)
            while c != None and c.activation:
                e = ut.randomPick(noeuds)
                s = ut.randomPick(noeudsSansEntree)
                c = self.genome.entreeSortieToCon(e,s)
                
            self.phenotype.modifierConnexion(e, s, self.idToPos, poids)
            if c != None:
                c.activer()
                c.poids = poids
            else:
                self.genome.ajouterConnexion(e,s,poids,innov)
    
    