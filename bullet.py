import pygame
from pygame.locals import *
import math

from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.r = 7
        self.angle = master.gun.angle
        self.color = [255, 0, 255]
        self.range = 700
        self.move(self.angle, 80)

    def repaint(self, screen, position):
        xy = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, xy, self.r)

    def update(self):
        self.move(self.angle, 30)
        field = self.master.master.field
        if self.range < 0 or field.touch(self):
            self.kill()

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        self.y += step * math.sin(angle)
        self.range -= step
    
    def kill(self):
        self.master.bullet.remove(self)
