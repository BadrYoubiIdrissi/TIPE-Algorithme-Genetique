# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 22:40:25 2017

@author: Badr Youbi Idrissi
"""

import pygame

class DataDisplay():
    def __init__(self, pos, centered = False, padding = 10):
        self.position = pos
        self.centered = centered
        self.padding = padding
        self.text = {}
        self.police = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        self.maxDigits = 5
    
    def add(self, label, value):
        self.text[label] = value
    
    def draw(self):
        screen = pygame.display.get_surface()
        xo, yo = self.position
        i = 0
        for label in self.text:
            rend = self.police.render(label + " : " + str(self.text[label]()), True, (0,0,0))
            if self.centered:
                x,y = xo - int(rend.get_width()/2) + self.padding, yo + 30*i + self.padding
            else:
                x,y = xo + self.padding, yo + 30*i + self.padding

            screen.blit(rend, (x,y))
            i += 1