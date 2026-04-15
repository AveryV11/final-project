import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1680, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pygame.display.set_caption("Submerged Survival")

clock = pygame.time.Clock()

difficulty_timer = 0

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
enemy_speed = 5

enemies = []

for i in range(3):
     x = random.randint(0, WIDTH - enemy_width)
     y = random.randint(-300, -50)
     enemies.append([x,y])

score = 0
last_spawn_score = 0
font = pygame.font.SysFont(None, 40)

game_over = False

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

def reset_game():
    global player_x, enemies, enemy_speed, score, game_over, last_spawn_score, difficutly_timer
    
    player_x = WIDTH // 2 - player_width // 2
    enemy_speed = 5
    score = 0
    game_over = False
    last_spawn_score = 0
    difficulty_timer = 0

    enemies = []
    for i in range(3):
        x = random.randint(0, WIDTH - enemy_width)
        y = random.randint(-300, -50)
        enemies.append([x, y])

while True:
    clock.tick(60)
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:

        difficulty_timer += 1

        if difficulty_timer % 600 == 0:
             enemy_speed *= 1.05

        if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
   
        for enemy in enemies:
            enemy[1] += enemy_speed

            if enemy[1] > HEIGHT:
                enemy[0] = random.randint(0, WIDTH - enemy_width)
                enemy[1] = random.randint(-200, -50)
                score += 1

            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)

            if player_rect.colliderect(enemy_rect):
                game_over = True

            pygame.draw.rect(screen, RED, enemy_rect)

        pygame.draw.rect(screen, WHITE, player_rect)

        if score % 10 == 0 and score != last_spawn_score and len(enemies) < 10:
             x = random.randint(0, WIDTH - enemy_width)
             y = random.randint(-200, -50)
             enemies.append([x, y])
             last_spawn_score = score

        draw_text(f"Score: {score}", 40, 10, 10)
    else:
        draw_text("GAME OVER", 60, WIDTH // 2 - 140, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", 40, WIDTH // 2 - 170, HEIGHT // 2 + 20)

    pygame.display.update()



