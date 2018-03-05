#-*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import json
import sys

from player import Player
import wall
import monster
import stuff

setting = json.load(open('setting.json', 'r'))
bg = setting['bg']
wh = setting['wh']

class Main:
    '''負責掌控主程序'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(wh)
        pygame.display.set_caption('FireWhell火輪手槍')

        #物件初始化
        self.clock = pygame.time.Clock()
        self.sound = pygame.mixer.Sound('data/sound/Jay_Jay.wav')
        self.sound.set_volume(0.5)

    def repaint(self, screen):
        '''將各個物件顯示到螢幕上。position為視野的座標，將此變數傳到各個物件，使物件在相對於座標的地方進行繪圖。repaint繼承自GameObject'''
        position = (self.player.x, self.player.y)
        screen.fill(bg)

        self.field.repaint(screen, position)
        self.player.repaint(screen, position)
        self.monster.repaint(screen, position)
        self.stuff.repaint(screen, position)
        pygame.display.flip()
        pygame.display.update()

    def update(self):
        '''物件更新'''
        self.player.update()
        self.field.update()
        self.monster.update()
        self.stuff.update()

    def gameover(self, screen, tops=[]):
        '''結束畫面'''
        screen.fill(bg) 
        position = (self.player.x, self.player.y)
        self.field.repaint(screen, position)
        self.player.repaint(screen, position)
        self.monster.repaint(screen, position)
        self.stuff.repaint(screen, position)
        f = pygame.font.Font('data/freesansbold.ttf', 90)
        text1 = f.render('Game Over', True, [255,255,100])
        text2 = f.render('Score: %s' % self.player.score, True, self.player.color)
        rect1 = text1.get_rect()
        rect2 = text2.get_rect()
        rect1.center = [wh[0]/2, wh[1]/2 - 300]
        rect2.center = [wh[0]/2, wh[1]/2 - 150]
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)

        f = pygame.font.Font('data/freesansbold.ttf', 50)
        for i in range(len(tops)):
            color = self.player.color if int(tops[i]) == self.player.score else [255,255,255]
            text = f.render('%s: %s' % (i+1, tops[i]), True, color)
            screen.blit(text, (wh[0]/2-100, wh[1]/2 + 50*(i-1)))

        pygame.display.flip()
        pygame.display.update()

    def reset(self):
        self.field = wall.Field(self)
        self.player = Player(self)
        self.monster = monster.MonsterManager(self)
        self.stuff = stuff.StuffManager(self)
        #self.sound.play(-1)

    def begin(self):
        '''主程序'''
        play = True     #設定遊戲狀態
        done = False
        self.reset()
        pygame.mixer.init()
        while not done:
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = True
                #設定全螢幕切換
                elif e.type is KEYDOWN :
                    if e.key == K_F11:
                        if self.screen.get_flags() & FULLSCREEN:
                            self.screen = pygame.display.set_mode(wh)
                        else:
                            self.screen = pygame.display.set_mode(wh, FULLSCREEN)

                    elif e.key == K_ESCAPE:
                        done = True
                    
                    elif e.key == K_SPACE:
                        self.player.shut()

                    elif e.key == K_RETURN and not play:
                        self.reset()
                        play = True
            if not play:
                self.gameover(self.screen, tops)    
            elif self.player.blood == 0:
                play = False
                sound.stop()
                tops = self.top(self.player.score)
                gameoverSound = pygame.mixer.Sound('data/sound/triumph.wav')
                gameoverSound.play()
            else:
                self.update()
                self.repaint(self.screen)
            self.clock.tick(30)

    @staticmethod
    def top(score):
        '''計算排行榜，排序分數，返回前七名並儲存到文件裡'''
        try:
            with open('data/score.txt', 'r') as file:
                data = file.read()
                score_list = data.split('\n')
        except FileNotFoundError:
            score_list = ['0' for i in range(7)]
        for s in range(len(score_list)):
            if score > int(score_list[s]):
                score_list.insert(s, str(score))
                break
        while len(score_list) > 7:
            del score_list[-1]
        with open('data/score.txt', 'w') as file:
            file.write('\n'.join(score_list))
        return score_list


root = Main()
root.begin()
