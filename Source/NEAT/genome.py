# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 12:21:44 2016

@author: Badr Youbi Idrissi

Un genome est un contennaire de connexions et de noeuds

C'est sur cet objet que va opérer les opérateurs génétiques
"""

class Genome():
    def __init__(self, connexions, noeuds):
        self.connexions = connexions
        self.noeuds = noeuds