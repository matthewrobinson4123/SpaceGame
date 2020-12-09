import pygame
import random
from SpaceBattle import(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from pygame import RLEACCEL

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/asteroid.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    # Move sprite by speed
    # Remove off screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()