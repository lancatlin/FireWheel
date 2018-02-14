import pygame
from pygame.locals import *
import math

from game_object import GameObject


distance = GameObject.setting['distance']

class Bullet(GameObject):
    def __init__(self, master, speed=50):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.r = 7
        self.angle = master.gun.angle + master.angle
        self.color = master.color
        self.range = 700
        self.a = self.master.a.copy()
        self.x += (distance-speed) * math.cos(self.angle)
        self.y += (distance-speed) * math.sin(self.angle)
        self.move(self.angle, speed)

    def repaint(self, screen, position):
        xy = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, xy, self.r)

    def update(self, touch):
        super().update(f = 0.95)
        speed = (self.a[0]**2 + self.a[1]**2) ** 0.5
        if speed < 10 or touch(): 
            self.kill()

    def kill(self):
        pass


class PlayerBullet(Bullet):
    def update(self):
        f = lambda:self.master.master.field.touch(self) or self.master.master.monster.touch(self)
        super().update(f)

    def kill(self):
        self.master.bullet.remove(self)


class SniperBullet(Bullet):
    def update(self):
        f = lambda:self.master.field.touch(self)
        super().update(f)

    def kill(self):
        self.master.master.bullet.remove(self)
        self.master.master.update_live()
        
