import json
import pygame


pygame.init()

class GameObject:
    setting = json.load(open('setting.json', 'r'))
    
    def __init__(self, master=None):
        self.master = master
        self.x = 0
        self.y = 0
        self.angle = 0
        self.color = []
        self.last_time = 0

    def repaint(self, screen, position):
        return int(self.x - position[0] + self.setting['wh'][0]/2), \
        int(self.y - position[1] + self.setting['wh'][1]/2)

    def update(self):
        pass

    def kill(self):
        pass
    
    @staticmethod
    def iskey(key):
        all_key = pygame.key.get_pressed()
        return all_key[key]
    
    def delay(self, time):
        return True if pygame.time.get_ticks() - self.last_time > time else False
