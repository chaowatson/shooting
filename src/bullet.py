import pygame.sprite


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
