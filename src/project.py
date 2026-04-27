import pygame
import random
import sys

WIDTH, HEIGHT = 1680, 850
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Submerged Survival")
clock = pygame.time.Clock()

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

submarine_img = pygame.image.load("submarine.png").convert_alpha()
scale_factor = 0.1
new_width = int(submarine_img.get_width() * scale_factor)
new_height = int(submarine_img.get_height() * scale_factor)

submarine_img = pygame.transform.scale(submarine_img, (new_width, new_height))

submarine_left = pygame.transform.flip(submarine_img, True, False)
submarine_right = submarine_img

submarine_mask_right = pygame.mask.from_surface(submarine_right)
submarine_mask_left = pygame.mask.from_surface(submarine_left)


difficulty_timer = 0

player_width = new_width
player_height = new_height

enemy_width = 120
enemy_height = 120

enemy_imgs = [
     pygame.image.load("enemy1.png").convert_alpha(),
     pygame.image.load("enemy2.png").convert_alpha(),
     pygame.image.load("enemy3.png").convert_alpha()
]

enemy_imgs = [pygame.transform.scale(img, (enemy_width, enemy_height)) for img in enemy_imgs]

enemy_masks = [pygame.mask.from_surface(img) for img in enemy_imgs]
enemy_speed = 5

player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7

enemies = []

for i in range(3):
     x = random.randint(0, WIDTH - enemy_width)
     y = random.randint(-600, -150)
     img_index = random.randint(0, 2)
     enemies.append([x, y, img_index])

score = 0
last_spawn_score = 0
font = pygame.font.SysFont(None, 40)

game_over = False

facing_right = True

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

def spawn_enemy():
     x = random.randint(0, WIDTH - enemy_width)
     y = random.randint(-600, -150)
     img_index = random.randint(0, 2)
     return [x, y, inm_index]

def reset_game():
    global player_x, enemies, enemy_speed, score, game_over, last_spawn_score, difficulty_timer
    
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
        img_index = random.randint(0, 2)
        enemies.append([x, y, img_index])

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
                facing_right = False

        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed
                facing_right = True

        player_rect = pygame.Rect(
             player_x + player_width * 0.2, 
             player_y + player_height * 0.2,
             player_width * 0.6,
             player_height * 0.6
        )

        for enemy in enemies:
            enemy[1] += enemy_speed

            if enemy[1] > HEIGHT:
                enemy[0] = random.randint(0, WIDTH - enemy_width)
                enemy[1] = random.randint(-600, -150)
                enemy[2] = random.randint(0, 2)
                score += 1

            enemy_rect = pygame.Rect(
                enemy[0] + 5,
                enemy[1] + 5,
                enemy_width - 10,
                enemy_height - 10
            )

            enemy_mask = enemy_masks[enemy[2]]

            offset_x = enemy[0] - player_x
            offset_y = enemy[1] - player_y

            if facing_right:
                collision = submarine_mask_right.overlap(enemy_mask, (offset_x, offset_y))
            else:
                collision = submarine_mask_left.overlap(enemy_mask, (offset_x, offset_y))

            if collision:
                game_over = True

            screen.blit(enemy_imgs[enemy[2]], (enemy[0], enemy[1]))
        if facing_right:
             screen.blit(submarine_right, (player_x, player_y))
        else:
             screen.blit(submarine_left, (player_x, player_y))
        

        if score % 10 == 0 and score != last_spawn_score and len(enemies) < 10:
             x = random.randint(0, WIDTH - enemy_width)
             y = random.randint(-200, -50)
             img_index = random.randint(0, 2)
             enemies.append([x, y, img_index])
             last_spawn_score = score

        draw_text(f"Score: {score}", 40, 10, 10)
    else:
        draw_text("GAME OVER", 60, WIDTH // 2 - 140, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", 40, WIDTH // 2 - 170, HEIGHT // 2 + 20)

    pygame.display.update()



