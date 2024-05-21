import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()
pygame.event.get()

image_pathA1 = 'alien.png'
image_pathBG = 'background.jpg'
image_pathSpS = 'spaceship.png'

alien = pygame.image.load(image_pathA1)
backGround = pygame.image.load(image_pathBG)
spaceship = pygame.image.load(image_pathSpS)

# Ustawienia ekranu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Ustawienia gracza
player_size = 50
player_pos = [screen_width / 2, screen_height - player_size]

# Ustawienia pocisków
bullet_size = 10
bullet_speed = 5
bullet_list = []

# Ustawienia kosmitów
enemy_size = 50
enemy_speed = 2
enemy_list = []

# Punkty i healthbar
score = 0
health = 100
clock = pygame.time.Clock()
game_over = False

# Główna pętla gry

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Strzelanie pociskami
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_pos = list(player_pos)
                bullet_pos[1] -= bullet_size
                bullet_list.append(list(bullet_pos))
                
    if health == 0:
        pygame.quit()
        sys.exit()

    screen.fill((0, 0, 0))

    # Inicjalizacja last_ticks
    last_ticks = pygame.time.get_ticks()

    # Ruch gracza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_pos[0] > 0:
            player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        if player_pos[0] < screen_width - player_size:
            player_pos[0] += 5

    # Rysowanie gracza
    pygame.draw.rect(screen, (0, 0, 255), (player_pos[0], player_pos[1], player_size, player_size))

    # Ruch i rysowanie pocisków
    for bullet in bullet_list:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_size, bullet_size))
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullet_list.remove(bullet)

    # Dodawanie nowych kosmitów
    if random.randint(0, 100) < 1:
        enemy_pos = [random.randrange(0, screen_width - enemy_size), 0]
        enemy_list.append({"pos": enemy_pos, "health": 2 if random.randint(0, 1) else 1})

    # Ruch i rysowanie kosmitów
    for enemy in list(enemy_list):
        enemy_pos = enemy["pos"]
        pygame.draw.rect(screen, (255, 0, 0), (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        enemy_pos[1] += enemy_speed

        # Kolizja z graczem
        if (enemy_pos[1] + enemy_size) > player_pos[1]:
            health -= 10
            enemy_list.remove(enemy)

        # Kolizja z pociskiem
        for bullet in list(bullet_list):
            if (bullet[0] >= enemy_pos[0] and bullet[0] < enemy_pos[0] + enemy_size) and (bullet[1] >= enemy_pos[1] and bullet[1] < enemy_pos[1] + enemy_size):
                bullet_list.remove(bullet)
                enemy["health"] -= 1
                if enemy["health"] <= 0:
                    enemy_list.remove(enemy)
                    score += 10

        # Healthbar
        pygame.draw.rect(screen, (0, 255, 0), (enemy_pos[0], enemy_pos[1] - 10, enemy_size * enemy["health"] / 2, 5))

    # Wyświetlanie punktów i healthbara
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {health}%", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)
