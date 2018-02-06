import pygame
from pygame.locals import *
import json
import math

from game_object import GameObject


wh = GameObject.setting['wh']
speed = GameObject.setting['speed']

class Player(GameObject):
    '''玩家物件，可以上下左右移動'''
    def __init__(self, master):
        self.x = int(wh[0] / 2)
        self.y = int(wh[1] / 2)
        self.r = 30
        self.color = [255, 0, 0]
        self.master = master
        self.gun = Gun(self)

    def repaint(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        self.gun.repaint(screen)

    def update(self):
        self.gun.update()


class Gun(GameObject):
    def __init__(self, master):
        self.master = master
        self.angle = 0
        self.x = self.master.x
        self.y = self.master.y

    def repaint(self, screen):
        far = 80
        xy = (int(self.x + math.cos(self.angle) * far), int(self.y + math.sin(self.angle) * far))
        pygame.draw.circle(screen, self.master.color, xy, 5)

    def update(self):
        self.x = self.master.x
        self.y = self.master.y
        self.angle += speed

    def shut(self, angle):
        pass

