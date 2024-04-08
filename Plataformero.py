import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
HEIGHT = int(HEIGHT)  # Convertir HEIGHT a entero
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
jump_count = 10  

platforms = []
traps = []

fall_speed = 0
gravity = 0.5
camera_speed = 5

game_over_image = pygame.image.load("gameover.png")
game_over_rect = game_over_image.get_rect()

player_jump_right = pygame.image.load("saltarD.png")
player_jump_left = pygame.image.load("saltarI.png")
player_idle_right = pygame.image.load("quietoD.png")
player_idle_left = pygame.image.load("quietoI.png")

platform_sprite_blue = pygame.image.load("saltarI.png")
platform_sprite_red = pygame.image.load("saltarI.png")

trap_sprite = pygame.image.load("saltarD.png")

player_image = player_idle_right  
clock = pygame.time.Clock()

def generate_platform():
    platform_width = random.randint(100, 200)
    platform_height = 20
    platform_x = random.randint(0, WIDTH - platform_width)
    platform_y = int(random.uniform(max(HEIGHT // 2, player_y + 100), HEIGHT + 200))
    platform_type = random.choice(["blue", "red"]) 
    return platform_x, platform_y, platform_width, platform_height, platform_type

def generate_trap():
    trap_width = 20  # Reducir el ancho de la trampa
    trap_height = 10  # Reducir la altura de la trampa
    trap_x = random.randint(0, WIDTH - trap_width)
    trap_y = random.randint(HEIGHT + 50, HEIGHT + 200)
    return trap_x, trap_y, trap_width, trap_height  # Actualizar las dimensiones de la trampa

def reset_level():
    global player_x, player_y, player_speed, is_jumping, jump_count
    global platforms, traps, fall_speed
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 2 * player_size
    player_speed = 5
    is_jumping = False
    jump_count = 10  
    platforms = []
    traps = []
    fall_speed = 0

reset_level()  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        player_image = player_idle_left
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
        player_image = player_idle_right

    if not is_jumping:
        if keys[pygame.K_SPACE] and player_y >= HEIGHT - player_size:
            is_jumping = True

    else:
        if jump_count >= -2:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    player_y -= camera_speed

    if random.randint(0, 100) < 3:  
        platforms.append(generate_platform())

    if random.randint(0, 100) < 3:
        traps.append(generate_trap())

    for i in range(len(platforms)):
        platforms[i] = (platforms[i][0], platforms[i][1] - camera_speed, platforms[i][2], platforms[i][3], platforms[i][4])

    for i in range(len(traps)):
        traps[i] = (traps[i][0], traps[i][1] - camera_speed, traps[i][2], traps[i][3])

    if player_y < HEIGHT - player_size:
        fall_speed += gravity
    player_y += fall_speed

    if player_y >= HEIGHT - player_size:
        fall_speed = 0  
        is_jumping = False

    for platform in platforms:
        if platform[4] == "blue" and platform[0] < player_x + player_size and platform[0] + platform[2] > player_x and platform[1] < player_y + player_size and platform[1] + platform[3] > player_y:
            player_y = platform[1] - player_size
            fall_speed = 0
            is_jumping = False

    for trap in traps:
        if trap[0] < player_x + player_size and trap[0] + trap[2] > player_x and trap[1] < player_y + player_size and trap[1] + trap[3] > player_y:
            print("Game Over - ¡Creo que no debiste tocar eso! :b ")
            screen.blit(game_over_image, (WIDTH // 2 - game_over_rect.width // 2, HEIGHT // 2 - game_over_rect.height // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            reset_level()  

    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size

    platforms = [platform for platform in platforms if platform[1] + platform[3] > 0]
    traps = [trap for trap in traps if trap[1] + trap[3] > 0]

    screen.fill(WHITE)
    screen.blit(player_image, (player_x, player_y))

    for platform in platforms:
        if platform[4] == "blue":
            screen.blit(platform_sprite_blue, (platform[0], platform[1]))
        elif platform[4] == "red":
            screen.blit(platform_sprite_red, (platform[0], platform[1]))

    for trap in traps:
        screen.blit(trap_sprite, (trap[0], trap[1] - trap[3]))  
    pygame.display.flip()
    clock.tick(60)
