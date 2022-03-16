import pygame.sprite
from .enemy import *
from .healthbar import *
from .wall import *

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







