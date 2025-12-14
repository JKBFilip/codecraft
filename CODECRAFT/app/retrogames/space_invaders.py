import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

import pygame
import sys
import random

# Inicjalizacja
pygame.init()

# Konfiguracja
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (200, 50, 255)  # Kolor pocisków wroga

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODECRAFT Space Invaders")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
pause_font = pygame.font.Font(None, 100)
quit_font = pygame.font.Font(None, 40)

# Gracz
player_width, player_height = 50, 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 5
bullets = []  # Pociski gracza

# Wrogowie
enemy_width, enemy_height = 40, 30
enemies = []
enemy_bullets = []  # Pociski wrogów
enemy_speed = 2
enemy_drop = 20
enemy_direction = 1

# Stan gry
score = 0
lives = 3
running = True
paused = False
game_over = False


def create_enemies():
    """Tworzy siatkę wrogów."""
    enemies.clear()
    enemy_bullets.clear()
    for row in range(5):
        for col in range(10):
            enemy = pygame.Rect(
                50 + col * (enemy_width + 15),
                50 + row * (enemy_height + 15),
                enemy_width,
                enemy_height
            )
            enemies.append(enemy)


def reset_game():
    global player_x, bullets, enemy_bullets, score, lives, game_over, enemy_speed
    player_x = WIDTH // 2 - player_width // 2
    bullets.clear()
    create_enemies()
    score = 0
    lives = 3
    enemy_speed = 2
    game_over = False


create_enemies()

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

            if paused and event.key == pygame.K_x:
                running = False

            if not paused and not game_over:
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 3:
                        bullet = pygame.Rect(player_x + player_width // 2 - 2, player_y, 4, 10)
                        bullets.append(bullet)

            if game_over and event.key == pygame.K_r:
                reset_game()

    # 2. Logika
    if not paused and not game_over:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
            player_x += player_speed

        # --- POCISKI GRACZA ---
        for b in bullets[:]:
            b.y -= 7
            if b.y < 0:
                bullets.remove(b)

        # --- RUCH WROGÓW ---
        move_down = False
        for e in enemies:
            e.x += enemy_speed * enemy_direction
            if e.right >= WIDTH or e.left <= 0:
                move_down = True

        if move_down:
            enemy_direction *= -1
            for e in enemies:
                e.y += enemy_drop
                if e.bottom >= player_y:  # Inwazja = Natychmiastowy koniec
                    game_over = True

        # --- STRZELANIE WROGÓW (NOWOŚĆ) ---
        # Szansa na strzał zależy od liczby wrogów (im mniej, tym wścieklejsi)
        shoot_chance = max(5, len(enemies) // 2)
        if random.randint(1, shoot_chance * 10) == 1 and enemies:
            shooter = random.choice(enemies)
            bullet = pygame.Rect(shooter.centerx, shooter.bottom, 4, 10)
            enemy_bullets.append(bullet)

        # Ruch pocisków wroga
        for eb in enemy_bullets[:]:
            eb.y += 5
            if eb.y > HEIGHT:
                enemy_bullets.remove(eb)

        # --- KOLIZJE ---
        # 1. Gracz trafia wroga
        for b in bullets[:]:
            for e in enemies[:]:
                if b.colliderect(e):
                    bullets.remove(b)
                    enemies.remove(e)
                    score += 10
                    enemy_speed += 0.05 if enemy_speed > 0 else -0.05
                    break

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # 2. Wróg trafia gracza (Utrata życia)
        for eb in enemy_bullets[:]:
            if eb.colliderect(player_rect):
                enemy_bullets.remove(eb)
                lives -= 1
                # Efekt trafienia (opcjonalnie można dodać mignięcie)
                if lives <= 0:
                    game_over = True
                break

        # 3. Wróg dotyka gracza (Kamikaze)
        for e in enemies:
            if e.colliderect(player_rect):
                lives = 0  # Natychmiastowa śmierć przy zderzeniu ciałami
                game_over = True

        # Respawn wrogów
        if not enemies:
            create_enemies()
            enemy_speed += 1

    # 3. Rysowanie
    screen.fill(BLACK)

    # Gracz
    pygame.draw.polygon(screen, NEON_GREEN, [
        (player_x + player_width // 2, player_y),
        (player_x, player_y + player_height),
        (player_x + player_width, player_y + player_height)
    ])

    # Wrogowie
    for e in enemies:
        pygame.draw.rect(screen, RED, e)
        # Oczy
        pygame.draw.rect(screen, BLACK, (e.x + 10, e.y + 10, 5, 5))
        pygame.draw.rect(screen, BLACK, (e.x + 25, e.y + 10, 5, 5))

    # Pociski gracza
    for b in bullets:
        pygame.draw.rect(screen, YELLOW, b)

    # Pociski wroga (Fioletowe)
    for eb in enemy_bullets:
        pygame.draw.rect(screen, PURPLE, eb)

    # UI
    score_text = font.render(f"Wynik: {score}", True, WHITE)
    lives_text = font.render(f"Życia: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    if game_over:
        over_text = pause_font.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, over_rect)

        restart_text = font.render("Naciśnij R, aby zagrać ponownie", True, WHITE)
        res_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(restart_text, res_rect)

    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pause_text = pause_font.render("PAUZA", True, WHITE)
        text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(pause_text, text_rect)

        sub_text = font.render("ESC - Powrót do gry", True, NEON_GREEN)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(sub_text, sub_rect)

        quit_text = quit_font.render("Naciśnij X aby wyjść z gry", True, (255, 100, 100))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(quit_text, quit_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()