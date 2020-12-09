# Import modules
import pygame
import Player
import Laser
import Enemy
import Star
# Import classes and constants from modules
from pygame import *

# Define screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Setup for music and sound playback
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom event for adding enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Create custom event for stars
ADDSTAR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDSTAR, 100)

# Instantiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# ADD BACKGROUND MUSIC
# Sound source: Dillon Robinson - artist Dillon Robinson
# pygame.mixer.music.load("sound/theme.ogg")
# pygame.mixer.music.play(loops=-1)
# pygame.mixer.music.set_volume(0.3)

# ADD SOUND FILES
# Sound Sources: Dillon Robinson
# explosion_sound = pygame.mixer.Sound("sound/explosion.ogg")
# shoot_sound = pygame.mixer.Sound("sound/shooting.ogg")

# Adjust volume levels
# explosion_sound.set_volume(0.5)
# shoot_sound.set_volume(0.5)

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

            elif event.key == K_SPACE:
                # shoot_sound.play()
                new_laser = Laser()
                lasers.add(new_laser)
                all_sprites.add(new_laser)


        # Did user click to close app? stop loop
        elif event.type == QUIT:
            running = False

        # Add an enemy?
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDSTAR:
            new_star = Star()
            stars.add(new_star)
            all_sprites.add(new_star)


    # Get the set of keys pressed and check for user input and then update
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update entity position
    enemies.update()
    stars.update()

    # Make screen black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check is enemies collide with player
    if pygame.sprite.spritecollideany(player, enemies):
        # explosion_sound.play()
        player.kill()
        pygame.time.delay(500)
        running = False

    for laser in lasers:
        for enemy in enemies:
            if pygame.sprite.spritecollideany(laser, enemies):
                # explosion_sound.play()
                enemy.kill()
                laser.kill()

    # Update display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop music
pygame.mixer.music.stop()
pygame.mixer.quit()


