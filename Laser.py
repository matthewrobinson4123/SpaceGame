import pygame
import random
from SpaceBattle import(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from pygame import RLEACCEL

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/bullet.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self):
        self.rect.move_ip(15, 0)