import pygame
import random
from SpaceBattle import(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from pygame import RLEACCEL

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/star.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    # Move star based on constant speed
    def update(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.kill()