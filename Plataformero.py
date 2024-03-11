import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5
jump_height = -15
is_jumping = False
jump_count = 10  # Número de frames para el salto

platforms = []
traps = []

fall_speed = 0
gravity = 1
camera_speed = 5

game_over_image = pygame.image.load("gameover.png")
game_over_rect = game_over_image.get_rect()

clock = pygame.time.Clock()

def generate_platform():
    platform_width = random.randint(50, 150)
    platform_height = 20
    platform_x = random.randint(0, WIDTH - platform_width)
    platform_y = random.randint(HEIGHT + 50, HEIGHT + 200)
    return platform_x, platform_y, platform_width, platform_height

def generate_trap():
    trap_width = 50
    trap_height = 20
    trap_x = random.randint(0, WIDTH - trap_width)
    trap_y = random.randint(HEIGHT + 50, HEIGHT + 200)
    return trap_x, trap_y, trap_width, trap_height

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Manejo del salto
    if not is_jumping:
        if keys[pygame.K_SPACE] and player_y >= HEIGHT - player_size:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    player_y -= camera_speed

    if random.randint(0, 100) < 7:
        platforms.append(generate_platform())

    if random.randint(0, 100) < 3:
        traps.append(generate_trap())

    for i in range(len(platforms)):
        platforms[i] = (platforms[i][0], platforms[i][1] - camera_speed, platforms[i][2], platforms[i][3])

    for i in range(len(traps)):
        traps[i] = (traps[i][0], traps[i][1] - camera_speed, traps[i][2], traps[i][3])

    if player_y < HEIGHT - player_size:
        fall_speed += gravity
    player_y += fall_speed

    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size
        fall_speed = 0
        is_jumping = False

    for platform in platforms:
        if platform[0] < player_x < platform[0] + platform[2] and \
                platform[1] <= player_y <= platform[1] + platform[3]:
            player_y = platform[1] - player_size
            fall_speed = 0
            is_jumping = False

    for trap in traps:
        if trap[0] < player_x < trap[0] + trap[2] and \
                trap[1] <= player_y <= trap[1] + trap[3]:
            print("Game Over - ¡Creo que no debiste tocar eso! :b ")
            screen.blit(game_over_image, (WIDTH // 2 - game_over_rect.width // 2, HEIGHT // 2 - game_over_rect.height // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

    if player_y >= HEIGHT - player_size:
        platforms.append(generate_platform())

    platforms = [platform for platform in platforms if platform[1] + platform[3] > 0]
    traps = [trap for trap in traps if trap[1] + trap[3] > 0]

    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))

    for platform in platforms:
        pygame.draw.rect(screen, RED, platform)

    for trap in traps:
        pygame.draw.rect(screen, BLUE, trap)

    pygame.display.flip()
    clock.tick(60)
 