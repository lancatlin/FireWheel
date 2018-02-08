import pygame
from pygame.locals import *

from game_object import GameObject

w = 50
h = 300

class Wall(GameObject):
    def __init__(self, master, position):
        super().__init__(master)
        self.x, self.y = position
        self.color = [255, 255, 255]
    
    def update(self):
        pass
    
    def repaint(self, screen, position):
        x, y = super().repaint(screen, position)
        pygame.draw.rect(screen, self.color, (x - w/2, y - h/2, w, h))
        pygame.draw.rect(screen, self.color, (x - h/2, y - w/2, h, w))
