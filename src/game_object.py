import random

import pygame.sprite
import math
from .param import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.display.init()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.image.convert()
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(20*TILESIZE, 15*TILESIZE)
        self.rot = 0
        self.rect = self.image.get_rect()
        self.rect.center = (20*TILESIZE, 15*TILESIZE)
        self.angle = 0

    def get_keys(self, motions):
        self.rot_speed = 0
        self.vel = pygame.math.Vector2(0, 0)
        for motion in motions:
            if motion == "UP":
                self.vel = pygame.math.Vector2(5, 0).rotate(-self.rot)
            elif motion == "DOWN":
                self.vel = pygame.math.Vector2(-5, 0).rotate(-self.rot)
            elif motion == "LEFT_TURN":
                self.rot_speed = 5
            elif motion == "RIGHT_TURN":
                self.rot_speed = -5


    def update(self, motions):
        print(self.rot)
        print(self.angle)
        print(self.rect.center)
        self.get_keys(motions)
        self.rot = self.rot + self.rot_speed
        self.angle = self.rot * math.pi / 180
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel

    @property
    def game_object_data(self):
        return {"type": "image",
                "name": "player",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle,
                "width": self.rect.width,
                "height": self.rect.height,
                "image_id": "player"
                }


class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([8, 8])
        self.color = "#E91E63"
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, 800)
        self.rect.centery = random.randint(0, 600)
        self.angle = 0

    def update(self) -> None:
        self.angle += 10
        if self.angle > 360:
            self.angle -= 360

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }
