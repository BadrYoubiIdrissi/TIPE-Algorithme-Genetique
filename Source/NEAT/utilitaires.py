# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 09:42:00 2016

Fonctions utiles:
    -Offset middle: Renvoie les coordonnés du milieu décalé de offset (utile pour affichage bezier)
    -Sigmoide: renvoie la sigmoide d'un vecteur (ou une matrice) terme à terme

@author: byoub
"""
import numpy as np


def offsetMiddle(pos1,pos2,off=15):
    x1, y1 = pos1
    x2, y2 = pos2
    xm, ym = (x1+x2)/2, (y1+y2)/2
    xo, yo = -(y2-y1),(x2-x1)
    norm = np.sqrt(xo**2+yo**2)
    return int(off*xo/norm+xm),int(off*yo/norm+ym)
    

def sigmoide(vect):
    return (1/(1+np.exp(-vect)))
