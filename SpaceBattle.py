# Import pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up loop using boolean variable
running = True
while running:
    # Look at every event in queue
    for event in pygame.event.get():
        # Did user hit a key?
        if event.type == KEYDOWN:
            # User hit escape? Stop loop
            if event.type == K_ESCAPE:
                running = False

        # Did user click to close app? stop loop
        if event.type == QUIT:
            running = False

    # Make screen white
    screen.fill((255, 255, 255))

    # Create surface
    surf = pygame.Surface((50, 50))

    # Give surface a color to separate from background
    surf.fill((0, 0, 0))
    rect = surf.get_rect()

    # Drawing onto screen
    screen.blit(surf, ((SCREEN_WIDTH-surf.get_width())/2, (SCREEN_HEIGHT-surf.get_height())/2))
    pygame.display.flip()


