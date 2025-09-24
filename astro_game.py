import pygame
import random
import sys

# test

# --- Initialize Pygame ---
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 630
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astro Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# --- Load Images ---
# 1. Spaceship
player_img_original = pygame.image.load("spaceship.png").convert_alpha()
player_img_original = pygame.transform.scale(player_img_original, (80, 80))

# 2. Background
background_img = pygame.image.load("background.jpg").convert()

# 3. Asteroid
asteroid_img_original = pygame.image.load("asteroid.png").convert_alpha()
asteroid_img_original = pygame.transform.scale(asteroid_img_original, (40, 40))

# --- Game variables ---
font = pygame.font.SysFont(None, 36)

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def game_over_screen(final_score):
    """Display game over and wait for SPACE to restart."""
    while True:
        screen.blit(background_img, (0, 0))
        draw_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2, RED)
        draw_text(f"Final Score: {final_score}", WIDTH // 2 - 90, HEIGHT // 2 + 40, WHITE)
        draw_text("Press SPACE to play again", WIDTH // 2 - 150, HEIGHT // 2 + 80, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return  # return to restart the game

        clock.tick(30)

def play_game():
    # --- Reset all game variables each time we play ---
    player_img = player_img_original.copy()
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 5

    bullets = []
    bullet_speed = 7

    asteroids = []
    asteroid_speed = 3
    asteroid_spawn_delay = 30  # frames
    asteroid_timer = 0

    score = 0
    lives = 3

    running = True
    while running:
        clock.tick(60)  # 60 FPS

        # --- Draw Background ---
        screen.blit(background_img, (0, 0))

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_SPACE]:
            # fire infinite bullets
            bullet_rect = pygame.Rect(player_rect.centerx - 2, player_rect.top - 10, 4, 10)
            bullets.append(bullet_rect)

        # --- Update Bullets ---
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # --- Spawn Asteroids ---
        asteroid_timer += 1
        if asteroid_timer > asteroid_spawn_delay:
            asteroid_timer = 0
            asteroid_rect = asteroid_img_original.get_rect(
                topleft=(random.randint(0, WIDTH - 40), -40)
            )
            asteroids.append(asteroid_rect)

        # --- Update Asteroids ---
        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.top > HEIGHT:
                asteroids.remove(asteroid)

        # --- Check Collisions (Bullets vs Asteroids) ---
        for asteroid in asteroids[:]:
            for bullet in bullets[:]:
                if asteroid.colliderect(bullet):
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 1  # 1 point per asteroid destroyed
                    break

        # --- Check Collisions (Asteroids vs Player) ---
        for asteroid in asteroids[:]:
            if asteroid.colliderect(player_rect):
                asteroids.remove(asteroid)
                lives -= 1
                if lives <= 0:
                    running = False  # end loop to show game over

        # --- Draw Player ---
        screen.blit(player_img, player_rect)

        # --- Draw Bullets (red) ---
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)

        # --- Draw Asteroids ---
        for asteroid in asteroids:
            screen.blit(asteroid_img_original, asteroid)

        # --- Draw Score and Lives ---
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", WIDTH - 100, 10)

        # --- Update Display ---
        pygame.display.flip()

    # After lives <= 0
    game_over_screen(score)

# --- Main Loop (keeps replaying) ---
while True:
    play_game()  # when play_game ends, show game_over_screen, then restart on SPACE
    