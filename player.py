import pygame
from pygame.locals import *
import json
import math

from game_object import GameObject
from bullet import PlayerBullet


wh = GameObject.setting['wh']
speed = GameObject.setting['speed']
distance = GameObject.setting['distance']

touchSound = pygame.mixer.Sound('data/sound/scream.wav')
touchSound.set_volume(0.2)
upSound = pygame.mixer.Sound('data/sound/fairydust.wav')
upSound.set_volume(1)

class Player(GameObject):
    '''玩家物件，可以上下左右移動'''
    def __init__(self, master):
        super().__init__(master)
        self.x = -200
        self.y = 100
        self.r = 30
        self.angle = 0
        self.color = [50, 200, 200]
        self.sound = pygame.mixer.Sound('data/sound/scream.wav')
        self.sound.set_volume(0.2)
        self.gun = Gun(self)
        self.bullet = []
        self.shuting = False
        self.speed = 2
        self.blood = 10
        self.score = 0
        self.level_factor = [0, 9]
        self.level = 0
        self.v = [0, 0]
        self.touchable = []
        self.next_score = self.next()
        
    def next(self):
        d = 5
        an = 10
        while True:
            an += d
            yield an + self.level_factor[-1]

    def repaint(self, screen, position):
        '''
        在此實做player的座標轉換是為了未來的鏡頭移動所準備，在實做此功能後，未來可維護性較高
        '''
        x, y = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, (x, y), self.r, 5)
        self.gun.repaint(screen, position)
        for b in self.bullet:
            b.repaint(screen, position)

        score = self.map(self.level_factor[-2], self.level_factor[-1], 0, 1000, self.score)
        score_block = Rect(170, 50, score, 30)
        pygame.draw.rect(screen, [0, 255, 255], score_block)
        for b in range(self.blood):
            pygame.draw.rect(screen, [255,0,0], (x-70+14*b, y-90, 10, 10))

        font = pygame.font.Font('data/freesansbold.ttf', 30)
        text = font.render('level: %s' % self.level, True, [255, 255, 255])
        screen.blit(text, (50,50))

    def update(self):
        '''更新狀態'''
        #如果分數超過最高就升等
        if self.score > self.level_factor[-1]:
            self.level += 1
            self.level_factor.append(next(self.next_score))
            upSound.play()

        zombie = self.master.monster.touch(self, True)
        #如果碰到殭屍、狙擊手、敵方子彈
        if self.delay(500) and zombie:
            self.last_time = pygame.time.get_ticks()
            self.blood -= 1
            #向反方向反彈
            self.near((zombie.x, zombie.y), -30)
            if zombie in self.master.monster.bullet:
                zombie.kill()
            touchSound.play()
        #更新玩家子彈
        for b in self.bullet:
            b.update()
        
        #如果按下按鍵就移動
        if self.iskey(K_w):
            self.v[1] += -self.speed
        if self.iskey(K_s):
            self.v[1] += self.speed
        if self.iskey(K_d):
            self.v[0] += self.speed
        if self.iskey(K_a):
            self.v[0] += -self.speed
        super().update(lambda :self.master.field.touch(self))
        
        #如果正在發射狀態就執行
        if self.shuting:
            self.shut()
        self.gun.update()
        
    def shut(self):
        #沒有在發射中，代表是第一次執行
        if not self.shuting:
            self.shuting = True
            self.gun.shuting = True
        #按鍵放開，結束發射模式
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
        self.angle = 0
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


