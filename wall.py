import pygame
from pygame.locals import *

from game_object import GameObject

w = 70
h = 400
g = 125

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

        
class Field(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.walls = []
        one_w = Wall(self, (0, 0))
        self.walls.append(one_w)
        a = (w + g)
        b = (w/2 + g + h/2)
        for i in range(4):
            self.walls.append(Wall(self, (one_w.x + a, one_w.y + b)))
            self.walls.append(Wall(self, (one_w.x - b, one_w.y + a)))
            self.walls.append(Wall(self, (one_w.x - a, one_w.y - b)))
            self.walls.append(Wall(self, (one_w.x + b, one_w.y - a)))
    
    def repaint(self, screen, position):
        for wall in self.walls:
            wall.repaint(screen, position)