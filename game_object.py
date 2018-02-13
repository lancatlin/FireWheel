import json
import pygame
import math


pygame.init()
F = 0.88

class GameObject:
    setting = json.load(open('setting.json', 'r'))
    
    def __init__(self, master=None):
        self.master = master
        self.x = 0
        self.y = 0
        self.a = [0, 0]
        self.angle = 0
        self.color = []
        self.last_time = 0
        self.touchable = []

    def repaint(self, screen, position):
        return int(self.x - position[0] + self.setting['wh'][0]/2), \
        int(self.y - position[1] + self.setting['wh'][1]/2)

    def update(self,touch=lambda:None, f=F):
        self.x += self.a[0]
        if touch():
            self.x -= self.a[0]
            self.a[0] = 0
        self.y += self.a[1]
        if touch():
            self.y -= self.a[1]
            self.a[1] = 0

        self.a = [x*f for x in self.a]

    def kill(self):
        pass
    
    @staticmethod
    def iskey(key):
        all_key = pygame.key.get_pressed()
        return all_key[key]
    
    def delay(self, time):
        return True if pygame.time.get_ticks() - self.last_time > time else False
    def near(self, position, step):
        x, y = self.x-position[0], self.y-position[1]
        distance = (x ** 2 + y ** 2) ** 0.5
        self.a[0] -= x/distance * step
        self.a[1] -= y/distance * step

    def move(self, angle, step):
        self.a[0] += step * math.cos(angle)
        self.a[1] += step * math.sin(angle)

    def be_touch(self):
        for i in self.touchable:
            if i.touch(self):
                return i
        else:
             return None
