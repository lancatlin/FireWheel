import pygame
from pygame.locals import *
import math

from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.angle = master.gun.angle
        self.color = [255, 0, 255]
        self.range = 500
        self.move(self.angle, 80)

    def repaint(self, screen, position):
        xy = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, xy, 5)

    def update(self):
        self.move(self.angle, 20)
        if self.range < 0:
            self.kill()

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        self.y += step * math.sin(angle)
        self.range -= step
    
    def kill(self):
        self.master.bullet.remove(self)
