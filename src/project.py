import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Submerged Survival")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

player_width = 60
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 7

enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -enemy_height
enemy_speed = 5

score = 0
font = pygame.font.SysFont(None, 40)

game_over = False

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

def reset_game():
    global player_x, enemy_x, enemy_y, enemy_speed, score, game_over
    player_x = WIDTH // 2 - player_width // 2
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = -enemy_height
    enemy_speed = 5
    score = 0
    game_over = False

while True:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        keys = pygame.key.get_pressed()

        if not game_over:
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed

            enemy_y += enemy_speed


