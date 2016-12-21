# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 09:42:00 2016

Fonctions utiles:
    -Offset middle: Renvoie les coordonnés du milieu décalé de offset (utile pour affichage bezier)
    -Sigmoide: renvoie la sigmoide d'un vecteur (ou une matrice) terme à terme
    -randomPick : renvoie un élément aléatoire de l'ensemble envoyé 

@author: byoub
"""
import numpy as np
import random as rand

def offsetMiddle(pos1,pos2,off=15):
    x1, y1 = pos1
    x2, y2 = pos2
    xm, ym = (x1+x2)/2, (y1+y2)/2
    xo, yo = -(y2-y1),(x2-x1)
    norm = np.sqrt(xo**2+yo**2)
    return int(off*xo/norm+xm),int(off*yo/norm+ym)
    

def sigmoide(vect):
    return (1/(1+np.exp(-vect)))

def randomPick(liste):
    return rand.sample(liste,1)[0]

def randomCoupleIf(range1, range2, nottest):
    a = randomPick(range1)
    b = randomPick(range2)
    i = 0
    while nottest(a,b):
        a = randomPick(range1)
        b = randomPick(range2)
        print(i, (a,b))
        i+=1
        if i == 10000:
            print(range1, range2)
            break
    return (a,b)