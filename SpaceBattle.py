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
    K_g,
    K_1,
)

# Define global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
score = 0
stage = 1
boss_spawned = False
god_mode = False
boss_alive = True
end_game_time = 0


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
    # Round 2
    if score == 100:
        stage += 1
    # Round 3
    elif score == 250:
        stage += 1
    # Round 4
    elif score == 550:
        stage += 1
    # Round 5
    elif score == 1000:
        stage += 1
    # Round 6
    elif score == 1600:
        stage += 1
    # Round 7
    elif score == 2350:
        stage += 1
    # Round 8
    elif score == 3250:
        stage += 1
    # Round 9
    elif score == 4300:
        stage += 1
    # Round 10
    elif score == 5500:
        stage += 1


# Define a Player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/Player.png")
        self.surf.set_colorkey((255, 255, 255,), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.lives = 1
        self.p1 = False
        self.shield = 0
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self, pressed_keys):
        #  reappear after death
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect = self.surf.get_rect()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on screen
        if not self.hidden:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    # shoot lasers
    def shoot(self):
        new_laser = Laser(self.rect.right, self.rect.centery, 0)
        lasers.add(new_laser)
        all_sprites.add(new_laser)
        if self.p1:
            upper_laser = Laser(self.rect.right, self.rect.centery, 1)
            lower_laser = Laser(self.rect.right, self.rect.centery, 2)
            lasers.add(upper_laser)
            lasers.add(lower_laser)
            all_sprites.add(upper_laser)
            all_sprites.add(lower_laser)
        shoot_sound.play()

    # temporarily hide player
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200)


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
        self.speed = random.randint(5, 9)
        self.just_shot = False

    # Move sprite by speed
    # Remove off screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    # add shooting for enemy
    def shoot(self):
        if not self.just_shot:
            new_laser = Laser(self.rect.left, self.rect.centery, 0)
            new_laser.speed = -new_laser.speed
            enemies.add(new_laser)
            all_sprites.add(new_laser)
            shoot_sound.play()
            self.just_shot = True
        else:
            self.just_shot = False


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
    def __init__(self, x, y, z):
        super().__init__()
        self.surf = pygame.image.load("images/bullet.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.speed = 15
        self.id = z

    # check what type of laser and update location on screen
    def update(self):
        if self.id == 0:
            self.rect.move_ip(self.speed, 0)
        elif self.id == 1:
            self.rect.move_ip(self.speed, 10)
        elif self.id == 2:
            self.rect.move_ip(self.speed, -10)
        if self.rect.left >= SCREEN_WIDTH or self.rect.right < 0:
            self.kill()


class PUP(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/powerup.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = -4
        self.id = random.randint(1, 3)

    # Move sprite by speed
    # Remove off screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/boss.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH + 100, SCREEN_HEIGHT/2 - 10)
        )
        self.speed = -3
        self.just_shot = False
        self.health = 500

    # Move boss onto screen
    def update(self):
        if self.rect.left > SCREEN_WIDTH - 250:
            self.rect.move_ip(self.speed, 0)

    # add shooting for boss
    def shoot(self):
        shot_type = random.randint(1, 10)
        if not self.just_shot:
            if shot_type <= 2:
                new_laser = Laser(self.rect.left, self.rect.centery, 0)
                bottom_laser = Laser(self.rect.left, self.rect.bottom, 0)
                top_laser = Laser(self.rect.left, self.rect.top, 0)
                top_laser.speed = bottom_laser.speed = new_laser.speed = -new_laser.speed
                enemies.add([new_laser, bottom_laser, top_laser])
                all_sprites.add([new_laser, bottom_laser, top_laser])
            elif 3 <= shot_type < 7:
                new_laser = Laser(self.rect.left, self.rect.centery, 0)
                upper_laser = Laser(self.rect.left, self.rect.centery, 1)
                lower_laser = Laser(self.rect.left, self.rect.centery, 2)
                lower_laser.speed = upper_laser.speed = new_laser.speed = -new_laser.speed
                enemies.add([new_laser, upper_laser, lower_laser])
                all_sprites.add([new_laser, upper_laser, lower_laser])
            elif shot_type >= 7:
                new_laser = Laser(self.rect.left, self.rect.centery, 0)
                upper_laser = Laser(self.rect.left, self.rect.centery, 1)
                lower_laser = Laser(self.rect.left, self.rect.centery, 2)
                top_laser = Laser(self.rect.left, self.rect.top, 0)
                top_upper_laser = Laser(self.rect.left, self.rect.top, 1)
                bottom_laser = Laser(self.rect.left, self.rect.bottom, 0)
                bottom_lower_laser = Laser(self.rect.left, self.rect.bottom, 2)
                bottom_lower_laser.speed = bottom_laser.speed = top_upper_laser.speed = top_laser.speed = lower_laser.speed = upper_laser.speed = new_laser.speed = -new_laser.speed
                enemies.add([new_laser, upper_laser, lower_laser, top_laser, top_upper_laser, bottom_laser, bottom_lower_laser])
                all_sprites.add([new_laser, upper_laser, lower_laser, top_laser, top_upper_laser, bottom_laser, bottom_lower_laser])
            shoot_sound.play()
            self.just_shot = True
        else:
            self.just_shot = False


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

# Create custom event for enemy shooting
SHOOT = pygame.USEREVENT + 4
pygame.time.set_timer(SHOOT, 500)

# Create custom event for power up spawning
POWER = pygame.USEREVENT + 5
pygame.time.set_timer(POWER, 5000)

# Instantiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
lasers = pygame.sprite.Group()
ships = pygame.sprite.Group()
pups = pygame.sprite.Group()
you = pygame.sprite.Group()
bosses = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
you.add(player)

# ---------------------------------------------------------------
#                set sounds and music
# ---------------------------------------------------------------
# Sound source: Dillon Robinson - artist Dillon Robinson
pygame.mixer.music.load('sounds/theme.wav')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
shoot_sound = pygame.mixer.Sound('sounds/shooting.wav')
powerup_pickup = pygame.mixer.Sound('sounds/powerup.wav')
boss_death_sound = pygame.mixer.Sound('sounds/bossdeath.wav')

# Adjust volume levels
explosion_sound.set_volume(0.5)
shoot_sound.set_volume(0.4)
powerup_pickup.set_volume(0.3)
boss_death_sound.set_volume(0.7)
# -----------------------------------------------------------------

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

            # God mode for debugging purposes
            elif event.key == K_g:
                if god_mode:
                    god_mode = False
                else:
                    god_mode = True
                    player.p1 = True

            elif event.key == K_SPACE:
                player.shoot()

            # Create pause button
            elif event.key == K_p:
                paused = True
                while paused:
                    for button in pygame.event.get():
                        if button.type == KEYDOWN:
                            if button.key == K_p:
                                paused = False

            if god_mode:
                if event.key == K_1:
                    score += 25
                    check_round()

        # Did user click to close app? stop loop
        elif event.type == QUIT:
            running = False

        elif event.type == ADDSTAR:
            new_star = Star()
            stars.add(new_star)
            all_sprites.add(new_star)

        elif event.type == POWER:
            new_pup = PUP()
            pups.add(new_pup)
            all_sprites.add(new_pup)

        # Add an enemy
        elif event.type == ADDENEMY:
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
                if stage >= 4:
                    if event.type == SHOOT:
                        for entity in ships:
                            num = random.randint(1, 10)
                            if num < 6:
                                entity.shoot()
            if stage == 10:
                if not boss_spawned:
                    boss = Boss()
                    bosses.add(boss)
                    all_sprites.add(boss)
                    boss_spawned = True
                if event.type == SHOOT:
                    num = random.randint(1, 10)
                    if num < 7:
                        boss.shoot()

        if score == 1000:
            pygame.event.clear()
            pygame.time.set_timer(ADDSHIP, 350)

        if score == 4300:
            pygame.time.set_timer(ADDENEMY, 200)

        if score == 5500:
            pygame.time.set_timer(SHOOT, 350)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('sounds/bosstheme.wav')
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.6)

    # Get the set of keys pressed and check for user input and then update
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    stars.update()
    lasers.update()
    pups.update()
    bosses.update()

    # Make screen black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check is enemies collide with player
    if not god_mode:
        if pygame.sprite.spritecollide(player, enemies, True):
            explosion_sound.play()
            if player.shield == 0:
                player.lives -= 1
                if player.lives == 0:
                    player.kill()
                    pygame.time.delay(1000)
                    running = False
                else:
                    player.hide()
                    player.p1 = False
            else:
                player.shield -= 20

    # Draw and update score on the screen
    draw_text(screen, str(score), 18, SCREEN_WIDTH / 2, 10)

    # Draw round number on screen
    draw_text(screen, "Round: {r}".format(r=stage), 30, SCREEN_WIDTH - 100, 10)

    # Draw player lives to screen
    draw_text(screen, "Lives: {l}".format(l=player.lives), 30, 80, SCREEN_HEIGHT - 50)

    # Draw player shield status
    draw_text(screen, "Shield: {s}".format(s=player.shield), 30, SCREEN_WIDTH/2, SCREEN_HEIGHT - 50)

    if boss_spawned:
        draw_text(screen, "BOSS HEALTH: {h}".format(h=boss.health), 20, SCREEN_WIDTH/2, 30)

    hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
    if hits:
        score += 25
        check_round()
        explosion_sound.play()

    for baddie in bosses:
        if pygame.sprite.spritecollide(baddie, lasers, True):
            boss.health -= 20
            if boss.health == 0:
                boss_death_sound.play()
                boss_alive = False
                boss.kill()
                end_game_timer = pygame.time.get_ticks()

    if not boss_alive:
        draw_text(screen, "YOU WIN", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if pygame.time.get_ticks() - end_game_timer > 2000:
            running = False

    for power in pups:
        if pygame.sprite.spritecollide(power, you, False):
            power.kill()
            powerup_pickup.play()
            for ship in you:
                if power.id == 1:
                    ship.p1 = True
                elif power.id == 2:
                    ship.shield = 100
                elif power.id == 3:
                    if player.lives < 3:
                        ship.lives += 1
                if ship.p1 and (ship.shield == 100) and (ship.lives == 3):
                    score += 50
                    check_round()

    # Update display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop music
pygame.mixer.music.stop()
pygame.mixer.quit()
