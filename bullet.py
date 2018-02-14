import pygame
from pygame.locals import *
import math

from game_object import GameObject


distance = GameObject.setting['distance']

class Bullet(GameObject):
    def __init__(self, master, speed=30):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.r = 7
        self.angle = master.gun.angle + master.angle
        self.speed = speed
        self.color = master.color
        self.range = 700
        self.a = self.master.a.copy()
        self.move(self.angle, distance)

    def repaint(self, screen, position):
        xy = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, xy, self.r)

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        self.y += step * math.sin(angle)
        self.range -= step

    def update(self, touch):
        self.move(self.angle, self.speed)
#super().update(f = 0.95)
        if self.range < 0 or touch(): 
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
    def __init__(self, master, speed=30):
        super().__init__(master, speed)
        self.score = 0

    def update(self):
        f = lambda:self.master.field.touch(self)
        super().update(f)

    def kill(self):
        self.master.master.bullet.remove(self)
        self.master.master.update_live()
        
