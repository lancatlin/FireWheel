import pygame
from pygame.locals import *
import math

from game_object import GameObject


class Bullet(GameObject):
    def __init__(self, master, a=(0,0)):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.r = 7
        self.angle = master.gun.angle
        self.color = [255, 0, 255]
        self.range = 700
        self.a = self.master.a.copy()
        self.x += 80 * math.cos(self.angle)
        self.y += 80 * math.sin(self.angle)
        self.move(self.angle, 50)

    def repaint(self, screen, position):
        xy = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, xy, self.r)

    def update(self):
        super().update(f = 0.95)
        field = self.master.master.field
        monster = self.master.master.monster
        speed = (self.a[0]**2 + self.a[1]**2) ** 0.5
        if speed < 10 or field.touch(self) or monster.touch(self):
            self.kill()

    def move(self, angle, step):
        super().move(angle, step)
    
    def kill(self):
        self.master.bullet.remove(self)
