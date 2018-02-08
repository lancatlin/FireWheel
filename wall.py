import pygame
from pygame.locals import *

from game_object import GameObject

w = 70
h = 500
g = 200

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
        mid = (0, 0)
        a = (w + g) / 2
        b = (w + g + h) / 2
        for i in range(10):
            self.add_wall(mid)
            mid = (mid[0] + 2*a, mid[1] + 2*b)
    
    def repaint(self, screen, position):
        for wall in self.walls:
            wall.repaint(screen, position)
    
    def add_wall(self, mid):
        a = (w + g) / 2
        b = (w + g + h) / 2
        self.walls.append(Wall(self, (mid[0] + a,mid[1] + b)))
        self.walls.append(Wall(self, (mid[0] - b,mid[1] + a)))
        self.walls.append(Wall(self, (mid[0] - a,mid[1] - b)))
        self.walls.append(Wall(self, (mid[0] + b,mid[1] - a)))