import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pygame")

import pygame
import sys
import random

# Inicjalizacja
pygame.init()

# Stałe
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
RED = (255, 50, 50)
DARK_GRAY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CODECRAFT Snake")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
pause_font = pygame.font.Font(None, 100)
quit_font = pygame.font.Font(None, 40)

# Stan gry
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Lista krotek (x, y)
direction = (0, 0)  # (dx, dy) - na początku stoi w miejscu
food = (0, 0)
score = 0
running = True
paused = False
game_over = False


def spawn_food():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)


def reset_game():
    global snake, direction, food, score, game_over
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # Start w prawo
    score = 0
    game_over = False
    food = spawn_food()


reset_game()
direction = (0, 0)  # Zatrzymujemy na start, żeby gracz się przygotował

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Pauza
            if event.key == pygame.K_ESCAPE:
                paused = not paused

            # Wyjście (tylko na pauzie)
            if paused and event.key == pygame.K_x:
                running = False

            # Sterowanie (tylko jeśli nie ma pauzy i nie game over)
            if not paused and not game_over:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)

            # Restart po game over
            if game_over and event.key == pygame.K_r:
                reset_game()

    # 2. Logika
    if not paused and not game_over:
        # Ruch tylko jeśli kierunek jest ustawiony (gra wystartowała)
        if direction != (0, 0):
            current_head = snake[0]
            new_head = (current_head[0] + direction[0], current_head[1] + direction[1])

            # Kolizja ze ścianą
            if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
                game_over = True

            # Kolizja z ogonem
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                # Jedzenie
                if new_head == food:
                    score += 1
                    food = spawn_food()
                    # Nie usuwamy ogona (wąż rośnie)
                else:
                    snake.pop()  # Usuwamy ogon (wąż przesuwa się)

    # 3. Rysowanie
    screen.fill(BLACK)

    # Siatka (opcjonalnie, dla efektu retro)
    # for x in range(0, WIDTH, GRID_SIZE):
    #     pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
    # for y in range(0, HEIGHT, GRID_SIZE):
    #     pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))

    # Jedzenie
    food_rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, food_rect)

    # Wąż
    for segment in snake:
        seg_rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, NEON_GREEN, seg_rect)
        # Opcjonalnie: ciemniejsza obwódka segmentu
        pygame.draw.rect(screen, BLACK, seg_rect, 1)

    # Wynik
    score_text = font.render(f"Wynik: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        over_text = pause_font.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, over_rect)

        restart_text = font.render("Naciśnij R, aby zagrać ponownie", True, WHITE)
        res_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(restart_text, res_rect)

    # Pauza
    if paused:
        # Tło pod napisem
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pause_text = pause_font.render("PAUZA", True, WHITE)
        text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(pause_text, text_rect)

        sub_text = font.render("ESC - Powrót do gry", True, NEON_GREEN)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(sub_text, sub_rect)

        quit_text = quit_font.render("X - Wyjście do menu", True, (255, 100, 100))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(quit_text, quit_rect)

    pygame.display.flip()
    # Prędkość gry (FPS) - można zwiększać wraz z wynikiem dla trudności
    speed = 10 + (score // 5)  # Co 5 punktów przyspieszamy o 1
    clock.tick(speed)

pygame.quit()
sys.exit()