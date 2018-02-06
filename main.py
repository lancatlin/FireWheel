import pygame
from pygame.locals import *
import json

from player import Player

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

        self.player = Player(self)
        self.clock = pygame.time.Clock()

    def repaint(self, screen):
        screen.fill(bg)

        self.player.repaint(screen)
        pygame.display.flip()
        pygame.display.update()

    def update(self):
        self.player.update()

    def begin(self):
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
                
            self.update()
            self.repaint(self.screen)
            self.clock.tick(30)


root = Main()
root.begin()
