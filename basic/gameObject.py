import json
import pygame
import math
import random
from abc import ABCMeta, abstractmethod

class GameObject:
    def __init__(self, master=None):
        self.master = master
        self.x = 0
        self.y = 0
        self.v = Vector(0, 0)
        self.angle = 0
        self.color = [0, 0, 0]
        self.lastTime = 0

    def callRepaint(self, screen, position):
        p = int(self.x - position.x + self.setting['wh'][0]/2, \
                int(self.y - position.y + self.setting['wh'][1]/2)
        self.repaint(screen, p)

    @abstractmethod
    def repaint(self, screen, pos):
        pass

    def callUpdate(self):
        self.update()

    def update(self, touch=lambda:None, f=0.88):
        self.x += self.v.x
        if touch():
            self.x -= self.v.x
            self.v.x = 0
        self.y += self.v.y
        if touch():
            self.y -= self.v.y
            self.v.y = 0

        self.v *= f

    @staticmethod
    def isKey(key):
        allKey = pygame.key.get_pressed()
        return allKey[key]

    def distance(self, person):
        return ((person.x - self.x)**2 + (person.y - self.y)**2) ** 0.5

    def move(self, angle, step):
        self.v.x += step * math.cos(angle)
        self.v.y += step * math.sin(angle)

    def near(self, person, step):
        x, y = self.x - person.x, self.y - person.y
        dis = self.distance(person)
        self.v.x -= x / dis * step
        self.v.y -= y / dis * step


