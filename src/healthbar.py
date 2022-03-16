import pygame.sprite


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