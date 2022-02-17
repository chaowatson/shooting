import random

import pygame.sprite
import math
from .param import *
from .map import *
from random import uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((32, 32))
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.rot = 0
        self.angle = 0
        self.last_shot = 0
        self.shot = 0
        self.shot_cool = 0

    def get_keys(self, motions):
        self.rot_speed = 0
        self.vel = pygame.math.Vector2(0, 0)
        for motion in motions:
            if motion == "UP":
                self.vel = pygame.math.Vector2(10, 0).rotate(-self.rot)
            elif motion == "DOWN":
                self.vel = pygame.math.Vector2(-10, 0).rotate(-self.rot)
            elif motion == "LEFT_TURN":
                self.rot_speed = 15
            elif motion == "RIGHT_TURN":
                self.rot_speed = -15
            elif motion == "SHOOT":
                if self.shot == 0:
                    dir = pygame.math.Vector2(1, 0).rotate(-self.rot)
                    pos = self.pos + pygame.math.Vector2(3,15).rotate(-self.rot)
                    Bullet(self.game, pos, dir)
                    self.vel = pygame.math.Vector2(-3, 0).rotate(-self.rot)
                    self.shot = 1


    def update(self, motions):
        self.shot_cool += 1
        if self.shot_cool % 5 == 0:
            self.shot = 0
        self.get_keys(motions)
        self.rot = self.rot + self.rot_speed
        self.angle = self.rot * math.pi / 180
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

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


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((8,8))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        #spread = uniform(-5, 5)
        self.vel = dir #dir.rotate(spread) * 1
        self.spawn_time = 0
        self.angle = 0


    def update(self):
        self.spawn_time += 1
        self.pos += self.vel*20
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if self.spawn_time > 10:
            self.kill()

    @property
    def game_object_data(self):
        return {"type": "image",
                "name": "bullet",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle,
                "width": self.rect.width,
                "height": self.rect.height,
                "image_id": "bullet"
                }