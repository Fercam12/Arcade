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

player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = player_size  # Modificado para que el jugador aparezca en la parte superior
player_speed = 10
jump_height = -15
is_jumping = False
jump_count = 10  

platforms = []
traps = []
score = 0
lives = 3  # Número de vidas inicial

fall_speed = 0
gravity = 0.3
camera_speed = 5

game_over_image = pygame.image.load("gameover.png")
game_over_rect = game_over_image.get_rect()

player_jump_right = pygame.image.load("saltarD.png")
player_jump_left = pygame.image.load("saltarI.png")
player_idle_right = pygame.image.load("quietoD.png")
player_idle_left = pygame.image.load("quietoI.png")

platform_sprite_blue = pygame.image.load("plataforma.png")
platform_sprite_red = pygame.image.load("plataforma.png")
score_platform_sprite = pygame.image.load("plataforma_special.png")  # Sprite de plataforma que otorga puntos

trap_sprite = pygame.image.load("trampa.png")

player_image = player_idle_right  
clock = pygame.time.Clock()

# Cargar imagen de fondo
background_image = pygame.image.load("fondo.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Fuente para el contador de tiempo
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks() // 1000  # Tiempo en segundos

# Ajustar la anchura de la plataforma al sprite
platform_width, platform_height = platform_sprite_blue.get_width(), 2

def generate_platform():
    platform_x = random.randint(0, WIDTH - platform_width)
    platform_y = int(random.uniform(max(HEIGHT // 2, player_y + 100), HEIGHT + 200))
    platform_type = random.choice(["blue", "red", "score"])  # Agregar tipo de plataforma que otorga puntos
    return platform_x, platform_y, platform_type

def generate_trap():
    trap_width = 7  # Reducir el ancho de la trampa
    trap_height = 3 # Reducir la altura de la trampa
    trap_x = random.randint(0, WIDTH - trap_width)
    trap_y = random.randint(HEIGHT + 25 , HEIGHT + 100)
    return trap_x, trap_y, trap_width, trap_height  # Actualizar las dimensiones de la trampa

def reset_level():
    global player_x, player_y, player_speed, is_jumping, jump_count, score, lives
    global platforms, traps, fall_speed, start_time  # Agregar start_time a las variables globales
    player_x = WIDTH // 2 - player_size // 2
    player_y = player_size  # Cambiar la posición inicial en y para que el jugador aparezca en la parte superior
    player_speed = 5
    is_jumping = False
    jump_count = 10  
    platforms = []
    traps = []
    fall_speed = 0
    start_time = pygame.time.get_ticks() // 1000  # Restablecer el tiempo de inicio
    lives -= 1  # Reducir el contador de vidas
    if lives <= 0:
        print("Game Over - ¡Creo que no debiste tocar eso! :b ")
        screen.blit(game_over_image, (WIDTH // 2 - game_over_rect.width // 2, HEIGHT // 2 - game_over_rect.height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        score = 0  # Reiniciar la puntuación si el jugador pierde todas las vidas
        lives = 3  # Reiniciar el número de vidas
    else:
        print("Has perdido una vida")
    reset_player_position()

def reset_player_position():
    global player_x, player_y
    player_x = WIDTH // 2 - player_size // 2
    player_y = player_size

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

    if random.randint(0, 100) < 0.8:
        traps.append(generate_trap())

    for i in range(len(platforms)):
        platforms[i] = (platforms[i][0], platforms[i][1] - camera_speed, platforms[i][2])

    for i in range(len(traps)):
        traps[i] = (traps[i][0], traps[i][1] - camera_speed, traps[i][2], traps[i][3])

    if player_y < HEIGHT - player_size:
        fall_speed += gravity
    player_y += fall_speed

    if player_y >= HEIGHT - player_size:
        fall_speed = 0  
        is_jumping = False

    for platform in platforms:
        if platform[0] < player_x + player_size and platform[0] + platform_width > player_x and platform[1] < player_y + player_size and platform[1] + platform_height > player_y:
            player_y = platform[1] - player_size
            fall_speed = 0
            is_jumping = False
            if platform[2] == "score":
                score += 25  # Incrementar la puntuación al tocar la plataforma que otorga puntos

    for trap in traps:
        if trap[0] < player_x + player_size and trap[0] + trap[2] > player_x and trap[1] < player_y + player_size and trap[1] + trap[3] > player_y:
            reset_level()
              
    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size

    platforms = [platform for platform in platforms if platform[1] + platform_height > 0]
    traps = [trap for trap in traps if trap[1] + trap[3] > 0]

    # Dibujar fondo de pantalla
    screen.blit(background_image, (0, 0))

    # Actualizar y mostrar el contador de tiempo
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    text = font.render("Tiempo: " + str(current_time) + "s", True, WHITE)
    screen.blit(text, (10, 10))

    # Mostrar puntuación
    score_text = font.render("Puntos: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    
    # Mostrar vidas
    lives_text = font.render("Vidas: " + str(lives), True, WHITE)
    screen.blit(lives_text, ((WIDTH - lives_text.get_width()) // 2, 10))

    screen.blit(player_image, (player_x, player_y))

    for platform in platforms:
        if platform[2] == "blue":
            screen.blit(platform_sprite_blue, (platform[0], platform[1]))
        elif platform[2] == "red":
            screen.blit(platform_sprite_red, (platform[0], platform[1]))
        elif platform[2] == "score":  # Dibujar la plataforma que otorga puntos
            screen.blit(score_platform_sprite, (platform[0], platform[1]))

    for trap in traps:
        screen.blit(trap_sprite, (trap[0], trap[1] - trap[3]))  
    pygame.display.flip()
    clock.tick(60)
