# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:56:54 2016

@author: Thomas Guilmeau
"""

class Noeud(object) :
    
    """
    Un noeud peut être une entrée, la sortie ou un gène intermédiaire (hidden gene)
    fonction peut prendre les valeurs "entree", "sortie" ou "cache"
    Chaque noeud a un identifiant unique qui permettera de faire le lien entre différents
    structures de réseau de neurones
    """
    
    def __init__(self, id, fonction):
        self.id = id
        self.fonction = fonction

