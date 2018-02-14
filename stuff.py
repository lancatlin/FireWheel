import pygame
from pygame.locals import *
import random

from game_object import *


h_capped = 15
s_capped = 60

class StuffManager(Manager):
    def __init__(self, master):
        super().__init__(master)
        self.hearts = []
        self.stars = []

    def repaint(self, screen, position):
        for h in self.stars+self.hearts:
            h.repaint(screen, position)

    def update(self):
        if self.delay(100):
            self.update_live()
            self.last_time = pygame.time.get_ticks()
        while len(self.hearts) < h_capped:
            self.hearts.append(Heart(self))
        while len(self.stars) < s_capped:
            self.stars.append(Star(self))
        for a in self.hearts+self.stars:
            a.update()


class Stuff(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.r = 10
        w, h = self.setting['field_wh']
        p = self.master.master.player
        self.x = random.uniform(min(p.x+1500, w), max(p.x-1500, -w))
        self.y = random.uniform(min(p.y+1500, h), max(p.y-1500, -h))
        self.player = self.master.master.player
        if self.master.master.field.touch(self, True):
            self.live = False
        else:
            self.live = True

    def repaint(self, screen, position):
        p = super().repaint(screen, position)
        if abs(p[0]) > 1500 or abs(p[1]) > 1500:
            self.live = False
        else:
            pygame.draw.circle(screen, self.color, p, self.r)

    def update(self):
        if not self.live:
            self.kill()
        elif self.touch():
            self.plus()
            self.kill()
        if self.master.master.field.touch(self, True):
            self.live = False

    def touch(self):
        d = ((self.x-self.player.x)**2 + (self.y-self.player.y)**2)**0.5
        if d < self.r + self.player.r:
            return True
        else:
            return False


class Heart(Stuff):
    def __init__(self, master):
        super().__init__(master)
        self.color = [255, 0, 0]

    def plus(self):
        self.player.blood += 1 if self.player.blood < 10 else 0

    def kill(self):
        self.master.hearts.remove(self)
        self.master.update_live()


class Star(Stuff):
    def __init__(self, master):
        super().__init__(master)
        self.color = [0, 255, 255]

    def plus(self):
        self.player.score += 1

    def kill(self):
        self.master.stars.remove(self)
        self.master.update_live()

