import pygame
from pygame.locals import *
import random

from game_object import GameObject


h_capped = 70
s_capped = 250

class StuffManager(GameObject):
    def __init__(self, master):
        self.master = master
        self.hearts = []
        self.stars = []
        self.live_hearts = []
        self.live_stars = []
        self.last_time = 0

    def repaint(self, screen, position):
        for h in self.live_hearts:
            h.repaint(screen, position)
        for s in self.live_stars:
            s.repaint(screen, position)

    def update(self):
        if self.delay(1000):
            self.update_live()
            self.last_time = pygame.time.get_ticks()
        elif len(self.hearts) < h_capped:
            self.hearts.append(Heart(self))
        elif len(self.stars) < s_capped:
            self.stars.append(Star(self))
        for a in self.live_hearts + self.live_stars:
            a.update()

    def update_live(self):
        p = self.master.player
        self.live_hearts = [h for h in self.hearts \
        if ((h.x-p.x)**2+(h.y-p.y)**2)**0.5 < 2000 ]
        self.live_stars = [s for s in self.stars \
        if ((s.x-p.x)**2+(s.y-p.y)**2)**0.5 < 2000 ]


class Stuff(GameObject):
    def __init__(self, master):
        super().__init__(master)
        self.r = 10
        w, h = self.setting['field_wh']
        self.x = random.randint(-w+1000, w-1000)
        self.y = random.randint(-h+1000, h-1000)
        self.player = self.master.master.player
        if self.master.master.field.touch(self, True):
            self.live = False
        else:
            self.live = True

    def repaint(self, screen, position):
        p = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, p, self.r)

    def update(self):
        if not self.live:
            self.kill()
        elif self.touch():
            self.plus()
            self.kill()

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

