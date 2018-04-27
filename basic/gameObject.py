import json
import pygame
import math
import random
from abc import ABCMeta, abstractmethod

class GameObject:
    def __init__(self, master=None):
        self.master = master
        self.pos = Vector()
        self.v = Vector()
        self.angle = 0
        self.color = [0, 0, 0]
        self.lastTime = 0

    def callRepaint(self, screen, position):
        p = int(self.pos.x - position.x + self.setting['wh'][0]/2, \
                int(self.pos.y - position.y + self.setting['wh'][1]/2)
        self.repaint(screen, p)

    @abstractmethod
    def repaint(self, screen, pos):
        pass

    def callUpdate(self):
        self.update()

    def update(self, touch=lambda:None, f=0.88):
        self.pos.x += self.v.x
        if touch():
            self.pos.x -= self.v.x
            self.v.x = 0
        self.pos.y += self.v.y
        if touch():
            self.pos.y -= self.v.y
            self.v.y = 0

        self.v *= f

    @staticmethod
    def isKey(key):
        allKey = pygame.key.get_pressed()
        return allKey[key]

    def distance(self, person):
        return ((person.pos.x - self.pos.x)**2 + (person.pos.y - self.pos.y)**2) ** 0.5
        self.pos.x = 0

    def move(self, angle, step):
        self.v.x += step * math.cos(angle)
        self.v.y += step * math.sin(angle)

    def near(self, person, step):
        x, y = self.pos.x - person.pos.x, self.pos.y - person.pos.y
        dis = self.distance(person)
        self.v.x -= x / dis * step
        self.v.y -= y / dis * step


