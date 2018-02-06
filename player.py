import pygame
from pygame.locals import *
import json


setting = json.load(open('setting.json', 'r'))
r = 30
wh = setting['wh']

class Player:
    '''玩家物件，可以上下左右移動'''
    def __init__(self, master):
        self.x = int(wh[0] / 2)
        self.y = int(wh[1] / 2)
        self.color = [255, 0, 0]
        self.master = master
        self.gun = Gun(self)

    def repaint(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), r)

    def update(self):
        pass


class Gun:
    def __init__(self, master):
        pass

    def repaint(self, screen):
        pass

    def update(self):
        pass

    def shut(self, angle):
        pass

