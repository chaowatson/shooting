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
        self.display_angle = 0
        self.hp = 100
        self.cd = False
        self.cd_count = 0
        self.healthbar = HealthBar(self.game,self,"#00FF00")
        self.last_shot = 0
        self.shot = 0
        self.shot_cool = 0
        self.north_distance = 0
        self.south_distance = 0
        self.west_distance = 0
        self.east_distance = 0
    def get_keys(self, motions):
        self.rot_speed = 0
        self.vel = pygame.math.Vector2(0, 0)
        for motion in motions:
            if motion == "UP":
                self.vel = pygame.math.Vector2(15, 0).rotate(-self.rot)
            elif motion == "DOWN":
                self.vel = pygame.math.Vector2(-15, 0).rotate(-self.rot)
            elif motion == "LEFT_TURN":
                self.rot_speed = 15
            elif motion == "RIGHT_TURN":
                self.rot_speed = -15
            elif motion == "SHOOT":
                if self.shot == 0:
                    dir = pygame.math.Vector2(1, 0).rotate(-self.rot)
                    pos = self.pos + pygame.math.Vector2(32, 0).rotate(-self.rot)
                    Bullet(self.game, pos, dir)
                    self.vel = pygame.math.Vector2(-3, 0).rotate(-self.rot)
                    self.shot = 1

    def step_back(self):
        self.vel = pygame.math.Vector2(-10, 0).rotate(-self.rot)

    def detect(self):
        north_max = 0
        south_min = 960
        west_max = 0
        east_min = 1216
        for wall in self.game.map.tmxdata.objects:
            if wall.name == 'Wall':
                if wall.x <= self.rect.centerx and (wall.x + 64) > self.rect.centerx:

                    if wall.y < self.rect.centery:
                        if wall.y > north_max:
                            self.north_distance = self.rect.y - wall.y - 64
                            north_max = wall.y
                        else:
                            self.north_distance = self.rect.y - north_max - 64
                    if wall.y > self.rect.centery:
                        if wall.y < south_min:
                            self.south_distance = wall.y - self.rect.y - 32
                            south_min = wall.y
                        else:
                            self.south_distance = south_min - self.rect.y - 32

                if wall.y <= self.rect.centery and (wall.y + 64) > self.rect.centery:

                    if wall.x < self.rect.centerx:
                        if wall.x > west_max:
                            self.west_distance = self.rect.x - wall.x - 64
                            west_max = wall.x
                        else:
                            self.west_distance = self.rect.x - west_max - 64
                    if wall.x > self.rect.centerx:
                        if wall.x < east_min:
                            self.east_distance = wall.x - self.rect.x - 32
                            east_min = wall.x
                        else:
                            self.east_distance = east_min - self.rect.x - 32

    def shoot_cd(self):
        self.shot_cool += 1
        if self.shot_cool % 5 == 0:
            self.shot = 0

    def injured_cd(self):
        self.cd = True

    def injured_cd_control(self):
        if self.cd:
            if self.cd_count > 20:
                self.cd = False
                self.cd_count = 0
            else:
                self.cd_count += 1

    def update(self, motions):

        self.detect()
        self.shot_cool += 1
        self.shoot_cd()
        self.get_keys(motions)
        self.rot = self.rot + self.rot_speed
        if self.rot >= 360 or self.rot <= -360:
            self.rot = 0
        self.angle = self.rot * math.pi / 180
        self.display_angle = self.rot
        if self.angle < 0:
            self.display_angle = self.display_angle + 360
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.injured_cd_control()
        Enemy.collide_with_enemies(self, self.game.enemies, 'x')
        Enemy.collide_with_enemies(self, self.game.enemies, 'y')
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        Wall.collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        Wall.collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        hit = pygame.sprite.spritecollideany(self, self.game.bullets)
        if pygame.sprite.spritecollideany(self, self.game.bullets):
            hit.kill()
            self.hp -= 30

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

    @staticmethod
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
        self.type = "enemy"

    def update(self):
        self.spawn_time += 1
        self.pos += self.vel*20
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if self.spawn_time > 30:
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


class EnemyFactory:

    @staticmethod
    def create_enemy(enemy_type, game, x, y, moving_path=None, speed=None):

        enemy = {'enemy': Enemy,
                 'enemy.left': Enemy.facing_left,
                 'enemy.right': Enemy.facing_right,
                 'enemy.down': Enemy.facing_down,
                 'enemy.up': Enemy.facing_up,
                 'moving enemy': MovingEnemy,
                 'shooting enemy.left': ShootingEnemy.facing_left,
                 'shooting enemy.right': ShootingEnemy.facing_right,
                 'shooting enemy.down': ShootingEnemy.facing_down,
                 'shooting enemy.up': ShootingEnemy.facing_up,
                 }

        return enemy[enemy_type](game, x, y, moving_path, speed)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, moving_path, speed):
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((32, 32))
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.rot = 270
        self.angle = -90 * math.pi / 180
        self.hp = 100
        self.healthbar = HealthBar(self.game, self, "#FF0000")


    def update(self):
        if self.hp < 1:
            self.kill()
            self.healthbar.kill()
        hit = pygame.sprite.spritecollideany(self, self.game.bullets)
        if pygame.sprite.spritecollideany(self, self.game.bullets):
            hit.kill()
            self.hp -= 30

    @property
    def game_object_data(self):
        return {"type": "image",
                "name": "enemy",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle,
                "width": self.rect.width,
                "height": self.rect.height,
                "image_id": "enemy"
                }

    @staticmethod
    def collide_with_enemies(sprite, group, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if not sprite.cd:
                    sprite.hp -= 30
                    sprite.injured_cd()
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    if sprite.display_angle <= 90 or sprite.display_angle >= 270:
                        sprite.vel = pygame.math.Vector2(50, 0).rotate(-sprite.rot)
                    else:
                        sprite.vel = pygame.math.Vector2(-50, 0).rotate(-sprite.rot)
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    if sprite.display_angle <= 90 or sprite.display_angle >= 270:
                        sprite.vel = pygame.math.Vector2(-50, 0).rotate(-sprite.rot)
                    else:
                        sprite.vel = pygame.math.Vector2(50, 0).rotate(-sprite.rot)

        if dir == 'y':
            hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if not sprite.cd:
                    sprite.hp -= 30
                    sprite.injured_cd()
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    if sprite.display_angle <= 180:
                        sprite.vel = pygame.math.Vector2(50, 0).rotate(-sprite.rot)
                    else:
                        sprite.vel = pygame.math.Vector2(-50, 0).rotate(-sprite.rot)
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    if sprite.display_angle <= 180:
                        sprite.vel = pygame.math.Vector2(-50, 0).rotate(-sprite.rot)
                    else:
                        sprite.vel = pygame.math.Vector2(50, 0).rotate(-sprite.rot)

    @classmethod
    def facing_left(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 180 * math.pi / 180
        return enemy

    @classmethod
    def facing_right(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 0
        return enemy

    @classmethod
    def facing_down(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 270 * math.pi / 180
        return enemy

    @classmethod
    def facing_up(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 90 * math.pi / 180
        return enemy

class MovingEnemy(Enemy):
    def __init__(self, game, x, y, moving_path: list, speed):
        super().__init__(game, x, y, moving_path, speed)
        self.type = "moving enemy"
        self.moving_path = moving_path
        self.path_index = 0
        self.speed = speed
        self.path_length = len(moving_path) - 1

    def move_control(self, moving_path):
        if self.path_index <= self.path_length:
            if moving_path[self.path_index] == '+x':
                self.vel = pygame.math.Vector2(self.speed, 0)
            elif moving_path[self.path_index] == '-x':
                self.vel = pygame.math.Vector2(-self.speed, 0)
            elif moving_path[self.path_index] == '+y':
                self.vel = pygame.math.Vector2(0, self.speed)
            elif moving_path[self.path_index] == '-y':
                self.vel = pygame.math.Vector2(0, -self.speed)
            self.path_index += 1
        else:
            self.path_index = 0

    def move(self):
        self.pos += self.vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        super(MovingEnemy, self).update()
        self.vel = pygame.math.Vector2(0, 0)
        self.move_control(self.moving_path)
        self.move()


class ShootingEnemy(Enemy):
    def __init__(self, game, x, y, moving_path: list, speed):
        super().__init__(game, x, y, moving_path, speed)
        self.type = "shooting enemy"
        self.shot = 0
        self.shot_cool = 0

    def shoot(self):
        if self.shot == 0:
            dir = pygame.math.Vector2(1, 0).rotate(-self.rot)
            pos = self.pos + pygame.math.Vector2(5, 0).rotate(-self.rot)
            Bullet(self.game, pos, dir)
            self.shot = 1

    def shoot_cd(self):
        self.shot_cool += 1
        if self.shot_cool % 40 == 0 or self.shot_cool % 40 == 10 :
            self.shot = 0


    def update(self):
        super(ShootingEnemy, self).update()
        self.rot = self.angle * 180/math.pi
        self.shoot()
        self.shoot_cd()

    @classmethod
    def facing_left(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 180 * math.pi / 180
        return enemy

    @classmethod
    def facing_right(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 0
        return enemy

    @classmethod
    def facing_down(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 270 * math.pi / 180
        return enemy

    @classmethod
    def facing_up(cls, game, x, y, moving_path, speed):
        enemy = cls(game, x, y, moving_path, speed)
        enemy.angle = 90 * math.pi / 180
        return enemy


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game,character,color):
        self.groups = game.all_sprites, game.healthbars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((32, 8))
        self.character = character
        self.angle = 0
        self.color = color


    @property
    def game_object_data(self):
        return {"type": "rect",
                "x": self.character.rect.x,
                "y": self.character.rect.y - 15,
                "angle": self.angle,
                "width": (32*self.character.hp)/100,
                "height": 4,
                "color": self.color,
                }
