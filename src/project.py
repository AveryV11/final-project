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

submarine_img = pygame.transform.scale(
    submarine_img, 
    (
        int(submarine_img.get_width() * scale_factor),
        int(submarine_img.get_height() * scale_factor)
    )
)

submarine_left = pygame.transform.flip(submarine_img, True, False)
submarine_right = submarine_img

submarine_mask_right = pygame.mask.from_surface(submarine_right)
submarine_mask_left = pygame.mask.from_surface(submarine_left)

player_width = submarine_img.get_width()
player_height = submarine_img.get_height

enemy_width = 120
enemy_height = 120

enemy_imgs = [
     pygame.image.load("enemy1.png").convert_alpha(),
     pygame.image.load("enemy2.png").convert_alpha(),
     pygame.image.load("enemy3.png").convert_alpha()
]

enemy_imgs = [pygame.transform.scale(img, (enemy_width, enemy_height)) for img in enemy_imgs]
enemy_masks = [pygame.mask.from_surface(img) for img in enemy_imgs]


def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

def spawn_enemy():
     x = random.randint(0, WIDTH - enemy_width)
     y = random.randint(-600, -150)
     img_index = random.randint(0, 2)
     return [x, y, img_index]

def reset_game():
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    enemies = [spawn_enemy() for _ in range(3)]

    return {
         "Player_x": player_x,
         "player_y": player_y, 
         "enemy_speed": enemies,
         "score": 0,
         "last_spawn_score": 0,
         "difficulty_time": 0,
         "game_over": False,
         "facing_right": True
    }
   
def handle_input(state):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and state["player_x"] > 0:
        state["player_x"] -= 7
        state["facing_right"] = False

    if keys[pygame.K_RIGHT] and state["player_x"] < WIDTH - player_width:
        state["player_x"] += 7
        state["facing_right"] = True

def update_enemies(state):
    for enemy in state["enemies"]:
            enemy[1] += state["enemy_speed"]

            if enemy[1] > HEIGHT:
                enemy[:] = spawn_enemy()
                state["score"] += 1

def check_collisions(state):
    for enemy in state["enemies"]:
        enemy_mask = enemy_masks[enemy[2]]

        offset_x = enemy[0] - state["player_x"]
        offset_y = enemy[1] - state["player_y"]

        if state["facing_right"]:
            collision = submarine_mask_right.overlap(enemy_mask, (offset_x, offset_y))
        else:
            collision = submarine_mask_left.overlap(enemy_mask, (offset_x, offset_y))

        if collision:
            state["game_over"] = True

def increase_difficulty(state):
    state["difficulty_timer"] += 1

    if state["difficulty_timer"] % 600 == 0:
        state["enemy_speed"] *= 1.05

    if (
        state["score"] % 10 == 0 and 
        state["score"] != state["last_spawn_score"] and
        len(state["enemies"]) , 10
    ):
        state["enemies"].append(spawn_enemy())
        state["last_spawn_score"] = state["score"]

def draw_game(state):
    screen.blit(background_img, (0, 0))

    for enemy in state["enemies"]:
        screen.blit(enemy_imgs[enemy[2]], (enemy[0], enemy[1]))

        if state["facing_right"]:
             screen.blit(submarine_right, (state["player_x"], state["player_y"]))
        else:
             screen.blit(submarine_left, (state["player_x"], state["player_y"]))

        draw_text(f"Score: {'score'}", 40, 10, 10)

def draw_game_over():
    draw_text("GAME OVER", 60, WIDTH // 2 - 140, HEIGHT // 2 - 50)
    draw_text("Press R to Restart", 40, WIDTH // 2 - 170, HEIGHT // 2 + 20)

def main():
    state = reset_game()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state["game_over"] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = reset_game()


        if not state["game_over"]:
            handle_input(state)
            update_enemies(state)
            check_collisions(state)
            increase_difficulty(state)
            draw_game(state)
        else:
            draw_game_over()

        pygame.display.update()

if __name__ == "__main__":
    main()