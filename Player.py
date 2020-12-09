# Import modules, classes, and constants
import pygame
# Import SpaceBattle
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

WIDTH = 0
HEIGHT = 0


# Define a Player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # define player size
        self.surf = pygame.Surface((75, 25))
        # colour player
        self.surf.fill((0, 255, 0,))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
