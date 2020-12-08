# Import modules
# Import classes and constants from modules
from Player import *


# Define screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Initialize pygame
pygame.init()

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player
player = Player()
player.WIDTH = SCREEN_WIDTH
player.HEIGHT = SCREEN_HEIGHT


# Set up loop using boolean variable
running = True
while running:
    # Look at every event in queue
    for event in pygame.event.get():
        # Did user hit a key?
        if event.type == KEYDOWN:
            # User hit escape? Stop loop
            if event.key == K_ESCAPE:
                running = False

        # Did user click to close app? stop loop
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update player location
    player.update(pressed_keys)

    # Make screen white
    screen.fill((255, 255, 255))

    # Draw player on screen
    screen.blit(player.surf, player.rect)

    # Update display
    pygame.display.flip()
