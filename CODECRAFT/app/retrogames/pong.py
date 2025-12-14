import warnings

# Wyciszamy ostrzeżenie o pkg_resources, które nie jest istotne dla naszej gry
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

import pygame
import sys

# Inicjalizacja
pygame.init()

# Konfiguracja
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODECRAFT Pong - Klasyk")
clock = pygame.time.Clock()

# Obiekty
paddle_w, paddle_h = 15, 90
ball_size = 15

# Gracz (lewa strona)
player = pygame.Rect(50, HEIGHT // 2 - paddle_h // 2, paddle_w, paddle_h)
# Komputer (prawa strona)
opponent = pygame.Rect(WIDTH - 50 - paddle_w, HEIGHT // 2 - paddle_h // 2, paddle_w, paddle_h)
# Piłka
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
opponent_speed = 5

score_p = 0
score_o = 0
font = pygame.font.Font(None, 74)
pause_font = pygame.font.Font(None, 100)  # Większa czcionka dla pauzy
quit_font = pygame.font.Font(None, 40)  # Mniejsza czcionka dla instrukcji wyjścia


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1


# Pętla gry
running = True
paused = False  # Nowa zmienna stanu pauzy

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Sterowanie Strzałki
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_DOWN:
                player_speed = 7

            # Sterowanie W/S (DODANE)
            if event.key == pygame.K_w:
                player_speed = -7
            if event.key == pygame.K_s:
                player_speed = 7

            # Pauza (ESC)
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Przełączamy stan

            # Wyjście z gry (X) - TYLKO PODCZAS PAUZY
            if paused and event.key == pygame.K_x:
                running = False

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                player_speed = 0

    # Jeśli jest pauza, pomijamy logikę gry i tylko rysujemy
    if not paused:
        # 2. Logika
        player.y += player_speed

        # Granice gracza
        if player.top < 0: player.top = 0
        if player.bottom > HEIGHT: player.bottom = HEIGHT

        # AI Przeciwnika (Proste śledzenie)
        if opponent.centery < ball.centery:
            opponent.y += opponent_speed
        if opponent.centery > ball.centery:
            opponent.y -= opponent_speed

        # Granice przeciwnika
        if opponent.top < 0: opponent.top = 0
        if opponent.bottom > HEIGHT: opponent.bottom = HEIGHT

        # Piłka
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Odbicia od ścian
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Odbicia od paletek
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
            # Przyspieszenie co odbicie
            ball_speed_x *= 1.05
            ball_speed_y *= 1.05

        # Punkty
        if ball.left <= 0:
            score_o += 1
            reset_ball()
            ball_speed_x = 6
            ball_speed_y = 6
        if ball.right >= WIDTH:
            score_p += 1
            reset_ball()
            ball_speed_x = -6
            ball_speed_y = 6

    # 3. Rysowanie
    screen.fill(BLACK)
    pygame.draw.aaline(screen, NEON_GREEN, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, NEON_GREEN, player)
    pygame.draw.rect(screen, NEON_GREEN, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)

    score_text = font.render(f"{score_p}", True, NEON_GREEN)
    screen.blit(score_text, (WIDTH // 2 - 60, 20))
    score_text_o = font.render(f"{score_o}", True, NEON_GREEN)
    screen.blit(score_text_o, (WIDTH // 2 + 20, 20))

    # Rysowanie ekranu PAUZY
    if paused:
        # Półprzezroczysta nakładka (opcjonalnie, tu prościej - napis na wierzchu)
        pause_text = pause_font.render("PAUZA", True, WHITE)
        text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Rysujemy tło pod napisem dla lepszej czytelności
        bg_rect = text_rect.inflate(40, 40)  # Trochę większe tło
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, NEON_GREEN, bg_rect, 3)  # Ramka

        screen.blit(pause_text, text_rect)

        # Instrukcja powrotu
        sub_text = font.render("Naciśnij ESC aby wrócić", True, NEON_GREEN)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(sub_text, sub_rect)

        # Instrukcja wyjścia (X)
        quit_text = quit_font.render("Naciśnij X aby wyjść z gry", True, (255, 100, 100))  # Lekko czerwony
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(quit_text, quit_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()