import pygame
from pygame.locals import *
import math

from game_object import GameObject


class Monster(GameObject):
    '''怪物的父類別'''
    def __init__(self, master):
        super().__init__(master)
        self.player = master.player
        self.speed = 8
        self.angle = 0
        self.color = [0, 255, 255]
        self.r = 30

    def repaint(self, screen, position):
        p = super().repaint(screen, position)
        pygame.draw.circle(screen, self.color, p, self.r)

    def update(self):
        self.move(self.angle, self.speed)

    def move(self, angle, step):
        self.x += step * math.cos(angle)
        if self.master.field.touch(self):
            self.x -= step * math.cos(angle)
        self.y += step * math.sin(angle)
        if self.master.field.touch(self):
            self.y -= step * math.sin(angle)

    def near(self, position, step):
        x, y = self.x-position[0], self.y-position[1]
        distance = (x ** 2 + y ** 2) ** 0.5
        self.x -= x/distance * step
        if self.master.field.touch(self):
            self.x += x/distance * step
        self.y -= y/distance * step
        if self.master.field.touch(self):
            self.y += y/distance * step


class Zombie(Monster):
    def __init__(self, master):
        super().__init__(master)
        self.x, self.y = -100, 10

    def update(self):
        x = self.x - self.player.x
        y = self.y - self.player.y
        self.near((self.player.x, self.player.y), self.speed)

