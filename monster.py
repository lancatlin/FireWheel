import pygame
from pygame.locals import *
import math
import random

from game_object import *
from player import Gun
from bullet import SniperBullet


z_capped = lambda x:20 + x*2
s_capped = lambda x:15 + x*2

class MonsterManager(Manager):
    def __init__(self, master):
        self.master = master
        self.last_time = 0
        self.player = master.player
        self.zombies = []
        self.snipers = []
        self.bullet = []
        self.live = []

    def update(self):
        if pygame.time.get_ticks() - self.last_time > 1000:
            self.update_live()
            super().update(self.zombies+self.snipers)
            self.last_time = pygame.time.get_ticks()
        elif len(self.zombies) < z_capped(self.player.level):
            self.zombies.append(Zombie(self))
        elif len(self.snipers) < s_capped(self.player.level):
            self.snipers.append(Sniper(self))
        for z in self.live:
            z.update()

    def touch(self, person):
        for z in self.live + self.bullet:
            if z.touch(person) and person is not z:
                if person in self.player.bullet:
                    z.kill()
                    self.player.score += 5
                return z
        else:
            return None

    def update_live(self):
        super().update_live(self.zombies+self.snipers+self.bullet)


class Monster(GameObject):
    '''怪物的父類別'''
    def __init__(self, master, position=None, color=None):
        super().__init__(master)
        self.player = master.player
        self.field = self.master.master.field
        self.speed = 1
        self.angle = 0
        self.color = [0, 255, 255]
        self.r = 30
        self.live = True
        self.range = lambda: 600 + self.player.level * 50 > self.distance(self)
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
        if self.field.touch(self, True):
            self.live = False
            self.color = [255, 255, 0]

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
        self.a[0] -= x/distance * step
        self.a[1] -= y/distance * step

    def touch(self, person):
        d = self.distance(person)
        return self if d < self.r+person.r else None

    def distance(self, person):
        return ((person.x - self.x)**2 + (person.y - self.y)**2) ** 0.5


class Zombie(Monster):
    def __init__(self, master):
        super().__init__(master)
        self.speed = 0.75

    def update(self):
        if self.range():
            self.near((self.player.x, self.player.y), self.speed)
        super().update(lambda :self.field.touch(self) or self.master.touch(self))
        if not self.live:
            self.kill()

    def kill(self):
        self.master.zombies.remove(self)
        self.master.update_live()

class Sniper(Monster):
    def __init__(self, master):
        super().__init__(master)
        self.speed = 1.5
        self.gun = Gun(self)
        self.angle = 0
        self.shuting = True
        self.gun.shuting = True
    
    def repaint(self, screen, position):
        super().repaint(screen, position)
        self.gun.repaint(screen, position)

    def update(self):
        x, y = self.x - self.player.x, self.y - self.player.y
        self.angle = math.atan(y/x)
        if x > 0:
            self.angle += math.pi
            pass
        d = (x**2 + y**2) ** 0.5
        if self.range():
            if d > 600:
                self.near((self.player.x, self.player.y), self.speed)
            elif pygame.time.get_ticks()-self.last_time > 1300:
                self.master.bullet.append(SniperBullet(self, 20))
                self.master.update_live()
                self.last_time = pygame.time.get_ticks()
            elif d < 400:
                self.near((self.player.x, self.player.y), -self.speed)
        super().update(lambda :self.field.touch(self) or self.master.touch(self))
        self.gun.update()

    def kill(self):
        self.master.snipers.remove(self)
        self.master.update_live()

