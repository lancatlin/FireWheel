#-*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import json

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
        print(type(self.screen))
        pygame.display.set_caption('FireWhell火輪手槍')

        self.field = wall.Field(self)
        self.player = Player(self)
        self.monster = monster.MonsterManager(self)
        self.stuff = stuff.StuffManager(self)
        self.clock = pygame.time.Clock()

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
        self.player.update()
        self.field.update()
        self.monster.update()
        self.stuff.update()

    def gameover(self, screen):
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
        rect1.center = [wh[0]/2, wh[1]/2 - 100]
        rect2.center = [wh[0]/2, wh[1]/2 + 100]
        screen.blit(text1, rect1)
        screen.blit(text2, rect2)

        pygame.display.flip()
        pygame.display.update()

    def begin(self):
        play = True
        pygame.mixer.init()
        sound = pygame.mixer.Sound('data/sound/Jay_Jay.wav')
        sound.play(-1)
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    exit()
                #設定全螢幕切換
                elif e.type is KEYDOWN :
                    if e.key == K_F11:
                        if self.screen.get_flags() & FULLSCREEN:
                            self.screen = pygame.display.set_mode(wh)
                            print(self.screen.get_size())
                        else:
                            self.screen = pygame.display.set_mode(wh, FULLSCREEN)
                            print(self.screen.get_size())

                    elif e.key == K_F12:
                        exit()
                    
                    elif e.key == K_SPACE:
                        self.player.shut()
            if not play:
                self.gameover(self.screen)    
            elif self.player.blood == 0:
                play = False
                sound.stop()
            else:
                self.update()
                self.repaint(self.screen)
            self.clock.tick(30)


root = Main()
root.begin()
