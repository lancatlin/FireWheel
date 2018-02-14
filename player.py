import pygame
from pygame.locals import *
import json
import math

from game_object import GameObject
from bullet import PlayerBullet


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
        self.color = [50, 200, 200]
        self.gun = Gun(self)
        self.bullet = []
        self.shuting = False
        self.speed = 2
        self.blood = 10
        self.score = 0
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

        score_block = Rect(100, 50, 10*(self.score % 100), 30)
        pygame.draw.rect(screen, [0, 255, 255], score_block)
        for b in range(self.blood):
            pygame.draw.rect(screen, [255,0,0], (x-70+14*b, y-90, 10, 10))

    def update(self):
        zombie = self.master.monster.touch(self)
        if self.delay(100) and zombie:
            self.last_time = pygame.time.get_ticks()
            self.blood -= 1
            self.near((zombie.x, zombie.y), -30)
            print(self.blood)
            if zombie in self.master.monster.bullet:
                zombie.kill()
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
            self.bullet.append(PlayerBullet(self))
            self.move(self.gun.angle, -6)
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
        xy = (int(x + math.cos(self.angle+self.master.angle) * distance), int(y + math.sin(self.angle+self.master.angle) * distance))
        pygame.draw.circle(screen, self.master.color, xy, 10)

    def update(self):
        self.x = self.master.x
        self.y = self.master.y
        self.angle += self.turn
        if self.angle > 270:
            self.angle-270
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
        elif not self.master.shuting:
            self.shuting = False
            self.turn *= 4
            self.last_time = 0


