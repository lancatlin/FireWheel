import pygame
from pygame.locals import *
import math
import random

from game_object import GameObject


z_capped = 50

class MonsterManager(GameObject):
    def __init__(self, master):
        self.master = master
        self.player = master.player
        self.last_time = 0
        self.zombies = []
        self.live_zombies = []

    def repaint(self, screen, position):
        for z in self.live_zombies:
            z.repaint(screen, position)

    def update(self):
        if pygame.time.get_ticks() - self.last_time > 1000:
            self.update_live()
            self.last_time = pygame.time.get_ticks()
        elif len(self.zombies) < z_capped:
            self.zombies.append(Zombie(self))
        for z in self.live_zombies:
            z.update()

    def touch(self, person):
        for z in self.live_zombies:
            if z.touch(person) and z is not person:
                if person in self.player.bullet:
                    z.kill()
                return z
        else:
            return None

    def update_live(self):
        p = self.player
        self.live_zombies = [z for z in self.zombies \
        if ((z.x-p.x)**2+(z.y-p.y)**2)**0.5 < 2000 ]



class Monster(GameObject):
    '''怪物的父類別'''
    def __init__(self, master, position=None, color=None):
        super().__init__(master)
        self.player = master.player
        self.field = self.master.master.field
        self.speed = 8
        self.angle = 0
        self.color = [0, 255, 255]
        self.r = 30
        if color:
            self.color = color
        else:
            self.color = [random.randint(100, 255) for i in range(3)]
        if position:
            self.x, self.y = position
        else:
            w, h = self.setting['field_wh']
            self.x = random.randint(-w+1000, w-1000)
            self.y = random.randint(-h+1000, h-1000)
        while self.field.touch(self, True):
            self.x += 5

    def repaint(self, screen, position):
        p = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, p, self.r)

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        if self.field.touch(self):
            self.x -= step * math.cos(angle)
        self.y += step * math.sin(angle)
        if self.field.touch(self):
            self.y -= step * math.sin(angle)

    def near(self, position, step):
        x, y = self.x-position[0], self.y-position[1]
        distance = (x ** 2 + y ** 2) ** 0.5
        self.x -= x/distance * step
        if self.field.touch(self) or self.master.touch(self):
            self.x += x/distance * step
        self.y -= y/distance * step
        if self.field.touch(self) or self.master.touch(self):
            self.y += y/distance * step

    def touch(self, person):
        distance = ((person.x - self.x)**2 + (person.y - self.y)**2) ** 0.5
        return self if distance < self.r+person.r else None


class Zombie(Monster):
    def __init__(self, master):
        super().__init__(master)

    def update(self):
        self.near((self.player.x, self.player.y), self.speed)

    def kill(self):
        self.master.zombies.remove(self)
        self.master.update_live()

