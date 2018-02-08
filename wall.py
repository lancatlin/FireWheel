import pygame
from pygame.locals import *
from pygame import Rect

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
        self.color = [255, 255, 255]
        self.w = 10000
        self.h = 10000
        self.edge = [Rect(-self.w, -self.h, 2*self.w, 100),
                     Rect(-self.w, -self.h, 100, 2*self.h),
                     Rect(-self.w, self.h-100, 2*self.w, 100),
                     Rect(self.w-100, -self.h, 100, 2*self.h)]
        self.walls = []
        mid = (0, 0)
        a = (w + g) / 2
        b = (w + g + h) / 2
        for i in range(10):
            self.add_wall(mid)
            mid = (mid[0], mid[1] + 2*g + 2*h - 2*w)
        mid = (0, 0)
        for i in range(10):
            self.add_wall(mid)
            mid = (mid[0] + 2*g + 2*h, mid[1])
    
    def repaint(self, screen, position):
        x, y = super().repaint(screen, position)
        for e in self.edge:
            paint_e = e.copy()
            paint_e.x += x
            paint_e.y += y
            pygame.draw.rect(screen, self.color, paint_e)
        for wall in self.walls:
            wall.repaint(screen, position)
    
    def add_wall(self, mid):
        a = (w + g) / 2
        b = (w + g + h) / 2
        self.walls.append(Wall(self, (mid[0] + a,mid[1] + b)))
        self.walls.append(Wall(self, (mid[0] - b,mid[1] + a)))
        self.walls.append(Wall(self, (mid[0] - a,mid[1] - b)))
        self.walls.append(Wall(self, (mid[0] + b,mid[1] - a)))