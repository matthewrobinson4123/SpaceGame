# Import modules
import pygame
import random

# Import classes and constants from modules
from pygame import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
    K_p,
)

# Define global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
score = 0
stage = 1

# Draw text onto screen
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text, text_rect)

# Check and update which round it is
def check_round():
    global stage
    if score == 100:
        stage += 1
    elif score == 250:
        stage += 1
    elif score == 550:
        stage += 1
    elif score == 1000:
        stage += 1
    elif score == 1600:
        stage += 1
    elif score == 2350:
        stage += 1
    elif score == 3250:
        stage += 1
    elif score == 4300:
        stage += 1
    elif score == 5500:
        stage += 1

# Define a Player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/Player.png")
        self.surf.set_colorkey((255, 255, 255,), RLEACCEL)
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
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        new_laser = Laser(self.rect.right, self.rect.centery)
        lasers.add(new_laser)
        all_sprites.add(new_laser)


# Define enemy class
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

# Define enemy ship class
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/EnemyShip.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 10 )

    # Move sprite by speed
    # Remove off screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the star object
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


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("images/bullet.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left >= SCREEN_WIDTH:
            self.kill()

# Setup for music and sound playback
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Set title for game
pygame.display.set_caption("Space Battle")

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom event for adding enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 400)

# Create custom event for stars
ADDSTAR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDSTAR, 100)

# Create custom event for ships
ADDSHIP = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSHIP, 600)

# Instantiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
lasers = pygame.sprite.Group()
ships = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# ADD BACKGROUND MUSIC
# Sound source: Dillon Robinson - artist Dillon Robinson
# pygame.mixer.music.load("sound/theme.wav")
# pygame.mixer.music.play(loops=-1)
# pygame.mixer.music.set_volume(0.3)

# ADD SOUND FILES
# Sound Sources: Dillon Robinson
# explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
# shoot_sound = pygame.mixer.Sound("sound/shooting.wav")

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
                player.shoot()

            # Create pause button
            elif event.key == K_p:
                paused = True
                while paused:
                    for button in pygame.event.get():
                        if button.type == KEYDOWN:
                            if button.key == K_p:
                                paused = False

        # Did user click to close app? stop loop
        elif event.type == QUIT:
            running = False

        elif event.type == ADDSTAR:
            new_star = Star()
            stars.add(new_star)
            all_sprites.add(new_star)

        # Add an enemy?

        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        if stage >= 3:
            if stage < 10:
                if event.type == ADDSHIP:
                    new_ship = Ship()
                    ships.add(new_ship)
                    enemies.add(new_ship)
                    all_sprites.add(new_ship)
            if stage == 4:
                pygame.time.set_timer(ADDSHIP, 400)

        if stage == 5:
            pygame.time.set_timer(ADDENEMY, 300)
            pygame.event.set_blocked(ADDSHIP)

    # Get the set of keys pressed and check for user input and then update
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    stars.update()
    lasers.update()

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

    # Draw and update score on the screen
    draw_text(screen, str(score), 18, SCREEN_WIDTH / 2, 10)

    # Draw round number on screen
    draw_text(screen, "Round: {r}".format(r=stage), 30, SCREEN_WIDTH - 100, 10)

    hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
    if hits:
        score += 25
        check_round()
        # explosion_sound.play()

    # Draw round number to screen

    # Update display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop music
pygame.mixer.music.stop()
pygame.mixer.quit()


