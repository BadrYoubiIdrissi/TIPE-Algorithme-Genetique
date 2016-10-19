# -*- coding: utf-8 -*-
"""
@author: Badr Youbi Idrissi
"""

import pygame

class NeuralNetRepr(pygame.sprite.Sprite):
    def __init__(self, genome):
        pygame.sprite.Sprite.__init__(self)
        self.genome = genome
        self.nodes = [pygame.Surface([10,10]) for i in range(len(genome.noeuds))]
        self.nodeRect = [self.nodes[i].get_rect() for i in range(len(genome.noeuds))]