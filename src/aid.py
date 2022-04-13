import pygame.sprite


class Aid(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.aids
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((64, 64))
        self.rect = pygame.Rect(x, y, 64, 64)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = 0

    @property
    def game_object_data(self):
        return {"type": "image",
                "name": "aid",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle,
                "width": self.rect.width,
                "height": self.rect.height,
                "image_id": "aid"
                }

    @staticmethod
    def get_position(game):
        position = []
        for aid in game.aids:
            position.append(f"{aid.rect.center}")
        return position