import pygame
from pygame.locals import *
import json
import math

from game_object import GameObject
from bullet import Bullet


wh = GameObject.setting['wh']
speed = GameObject.setting['speed']
distance = GameObject.setting['distance']

class Player(GameObject):
    '''玩家物件，可以上下左右移動'''
    def __init__(self, master):
        super().__init__(master)
        self.x = -200
        self.y = 100
        self.r = 30
        self.color = [255, 0, 0]
        self.gun = Gun(self)
        self.bullet = []
        self.shuting = False
        self.speed = 2
        self.blood = 10
        self.a = [0, 0]
        self.touchable = []

    def repaint(self, screen, position):
        '''
        在此實做player的座標轉換是為了未來的鏡頭移動所準備，在實做此功能後，未來可維護性較高
        '''
        x, y = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, (x, y), self.r)
        self.gun.repaint(screen, position)
        for b in self.bullet:
            b.repaint(screen, position)

        blood_block = Rect(100, 50, 100*self.blood, 50)
        pygame.draw.rect(screen, [255, 0, 0, 100], blood_block)

    def update(self):
        zombie = self.master.monster.touch(self)
        if self.delay(100) and zombie:
            self.last_time = pygame.time.get_ticks()
            self.blood -= 1
            self.near((zombie.x, zombie.y), -30)
            print(self.blood)
        for b in self.bullet:
            b.update()
        
        if self.iskey(K_w):
            self.a[1] += -self.speed
        if self.iskey(K_s):
            self.a[1] += self.speed
        if self.iskey(K_d):
            self.a[0] += self.speed
        if self.iskey(K_a):
            self.a[0] += -self.speed
        super().update(lambda :self.master.field.touch(self))
        if self.shuting:
            self.shut()
        self.gun.update()
        
    def shut(self):
        if not self.shuting:
            self.shuting = True
            self.gun.shuting = True
        elif not self.iskey(K_SPACE):
            self.bullet.append(Bullet(self))
            self.move(self.gun.angle, -8)
            self.shuting = False



class Gun(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.x = self.master.x
        self.y = self.master.y
        self.turn = speed
        self.shuting = False
        self.last_time = 0

    def repaint(self, screen, position):
        x, y = super().repaint(screen, position)
        xy = (int(x + math.cos(self.angle) * distance), int(y + math.sin(self.angle) * distance))
        pygame.draw.circle(screen, self.master.color, xy, 10)

    def update(self):
        self.x = self.master.x
        self.y = self.master.y
        self.angle += self.turn
        if self.shuting:
            self.shut()

    def shut(self):
        #如果第一次按下
        if self.last_time == 0:
            self.turn *= -0.25
            self.last_time = pygame.time.get_ticks()
        #如果超過一秒，換方向
        elif pygame.time.get_ticks() - self.last_time > 500:
            self.turn *= -1
            self.last_time = pygame.time.get_ticks()
        #如果按鍵已放開
        elif not Gun.iskey(K_SPACE):
            self.shuting = False
            self.turn *= 4
            self.last_time = 0


