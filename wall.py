import pygame
from pygame.locals import *

from game_object import GameObject

class Wall(GameObject):
    def __init__(self, master, position):
        super().__init__(master)
        self.x, self.y = position
        self.color = [255, 255, 255]
    
    def update(self):
        pass
    
    def repaint(self, screen, position):
        x, y = super().repaint(screen, position)
        pygame.draw.rect(screen, self.color, )
