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
        self.shuting = False

    def repaint(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        self.gun.repaint(screen)
        for b in self.bullet:
            b.repaint(screen)

    def update(self):
        self.gun.update()
        for b in self.bullet:
            b.update()
        if self.shuting:
            self.shut()

    def shut(self):
        if not self.shuting:
            self.shuting = True
            self.gun.shuting = True
        elif not self.iskey(K_SPACE):
            self.bullet.append(Bullet(self))
            self.shuting = False


class Gun(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = self.master.x
        self.y = self.master.y
        self.change = speed
        self.shuting = False
        self.last_time = 0

    def repaint(self, screen):
        xy = (int(self.x + math.cos(self.angle) * distance), int(self.y + math.sin(self.angle) * distance))
        pygame.draw.circle(screen, self.master.color, xy, 10)

    def update(self):
        self.x = self.master.x
        self.y = self.master.y
        self.angle += self.change
        if self.shuting:
            self.shut()

    def shut(self):
        #如果第一次按下
        if self.last_time == 0:
            self.change *= -0.25
            self.last_time = pygame.time.get_ticks()
        #如果超過一秒，換方向
        elif pygame.time.get_ticks() - self.last_time > 500:
            self.change *= -1
            self.last_time = pygame.time.get_ticks()
        #如果按鍵已放開
        elif not Gun.iskey(K_SPACE):
            self.shuting = False
            self.change *= 4
            self.last_time = 0


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

