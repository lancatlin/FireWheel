import pygame
from pygame.locals import *
import json
import math

from game_object import GameObject


wh = GameObject.setting['wh']
speed = GameObject.setting['speed']
distance = GameObject.setting['distance']

class Player(GameObject):
    '''玩家物件，可以上下左右移動'''
    def __init__(self, master):
        super().__init__(master)
        self.x = int(wh[0] / 2)
        self.y = int(wh[1] / 2)
        self.r = 30
        self.color = [255, 0, 0]
        self.gun = Gun(self)
        self.bullet = []

    def repaint(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        self.gun.repaint(screen)
        for b in self.bullet:
            b.repaint(screen)

    def update(self):
        self.gun.update()
        for b in self.bullet:
            b.update()

    def shut(self):
        self.bullet.append(Bullet(self))
        self.gun.shut()


class Gun(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = self.master.x
        self.y = self.master.y

    def repaint(self, screen):
        xy = (int(self.x + math.cos(self.angle) * distance), int(self.y + math.sin(self.angle) * distance))
        pygame.draw.circle(screen, self.master.color, xy, 10)

    def update(self):
        self.x = self.master.x
        self.y = self.master.y
        self.angle += speed

    def shut(self):
        pass


class Bullet(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = master.x
        self.y = master.y
        self.angle = master.gun.angle
        self.color = [255, 255, 255]
        self.move(self.angle, 80)

    def repaint(self, screen):
        xy = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, xy, 5)

    def update(self):
        self.move(self.angle, 10)
        if self.x < 0 or self.x > wh[0] or self.y < 0 or self.y > wh[1]:
            self.kill()

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        self.y += step * math.sin(angle)
    
    def kill(self):
        self.master.bullet.remove(self)

