import pygame.sprite

import math
from .healthbar import *
from .wall import *
from .bullet import *
from .map import *

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
