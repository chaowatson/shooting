import pygame
import pytmx
from .param import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class TiledMap:
    def __init__(self, filename):
        pygame.display.init()
        pygame.display.set_mode((WIDTH, HEIGHT))
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
