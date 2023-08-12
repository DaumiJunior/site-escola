import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações da janela do jogo
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meu Jogo")

# Variáveis do jogador
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2  # Posição inicial no centro horizontal
player_y = screen_height - player_height - 20
player_speed = 5
player_lives = 3
player_score = 0
player_level = 1
has_weapon = False
points_since_last_weapon = 0

# Variáveis do inimigo
enemy_width = 30
enemy_height = 30
enemy_speed = 25  # Movimento de 25 pixels por segundo
enemy_speed_increase = 1.5  # Fator de aumento de velocidade a cada nível

# Variáveis dos pontos verdes
point_radius = 10
points = []
points_per_minute = 30  # Aumente para aumentar a velocidade de surgimento dos pontos
points_spawn_interval = 2.0  # Intervalo de 2 segundos para gerar um novo ponto verde

# Variáveis dos inimigos
enemies = []
max_enemies = 30
current_enemies = 2  # Quantidade inicial de inimigos
enemies_per_level = 3  # Quantidade de inimigos adicionados por nível
enemy_spawn_interval = 7000  # Intervalo de 7 segundos em milissegundos
last_enemy_spawn_time = 0  # Variável para armazenar o momento do último spawn de inimigo

# Variáveis dos projéteis
projectile_radius = 5
projectile_speed = 15  # Velocidade dos projéteis
projectiles = []
# Variáveis de respawn dos inimigos
enemy_respawn_time = 7  # Tempo em segundos para respawn dos inimigos
enemy_respawn_timer = 0

# Variáveis de invencibilidade após colisão
invincible_time = 3  # Tempo em segundos
is_invincible = False
invincible_timer = 0

# Inicialização do clock para controlar o FPS
clock = pygame.time.Clock()

# Função para obter o tempo decorrido entre atualizações
def get_delta_time():
    return clock.get_time() / 1000.0  # Converter o tempo em segundos

# Função para gerar um novo ponto verde aleatoriamente
def spawn_point():
    point_x = random.randint(0, screen_width - 2 * point_radius)
    point_y = random.randint(0, screen_height - 2 * point_radius)
    points.append((point_x, point_y))

# Função para gerar um novo inimigo aleatoriamente em qualquer ponto da tela
def spawn_enemy():
    global enemies, current_enemies

    side = random.randint(1, 4)  # Escolhe um lado (1: superior, 2: inferior, 3: esquerdo, 4: direito)
    if side == 1:  # Superior
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
    elif side == 2:  # Inferior
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = screen_height
    elif side == 3:  # Esquerdo
        enemy_x = -enemy_width
        enemy_y = random.randint(0, screen_height - enemy_height)
    elif side == 4:  # Direito
        enemy_x = screen_width
        enemy_y = random.randint(0, screen_height - enemy_height)

    # Aumenta a velocidade do inimigo a cada novo nível
    enemy_speed = enemy_speed_increase * player_level
    enemies.append([enemy_x, enemy_y, enemy_speed])

# Função para gerar novos inimigos quando necessário
def spawn_enemies():
    global current_enemies, last_enemy_spawn_time

    if len(enemies) < max_enemies and current_enemies > 0:
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time >= enemy_spawn_interval:
            last_enemy_spawn_time = current_time
            for _ in range(current_enemies):
                spawn_enemy()
            current_enemies -= 1  # Diminuir o contador de inimigos

# Função para verificar colisões entre o jogador e os inimigos
def check_collisions_with_enemies():
    global player_lives, is_invincible, invincible_timer

    if not is_invincible:
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2

        new_enemies = []
        for enemy in enemies:
            enemy_center_x = enemy[0] + enemy_width // 2
            enemy_center_y = enemy[1] + enemy_height // 2

            dx = player_center_x - enemy_center_x
            dy = player_center_y - enemy_center_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance < (player_width // 2 + enemy_width // 2):
                # Reduz a vida do jogador quando colidir com um inimigo
                player_lives -= 1
                is_invincible = True
                invincible_timer = invincible_time
                # Empurra o inimigo para longe do jogador (inverte a direção)
                direction_x = dx / distance
                direction_y = dy / distance
                enemy[0] += direction_x * enemy_speed * 3
                enemy[1] += direction_y * enemy_speed * 3
            else:
                new_enemies.append(enemy)
        enemies.clear()
        enemies.extend(new_enemies)

# Função para verificar colisões entre o jogador e os pontos verdes
def check_collisions_with_points():
    global player_score, has_weapon, points_since_last_weapon, player_level, player_lives

    player_center_x = player_x + player_width // 2
    player_center_y = player_y + player_height // 2

    new_points = []
    for point in points:
        point_center_x = point[0] + point_radius
        point_center_y = point[1] + point_radius

        dx = player_center_x - point_center_x
        dy = player_center_y - point_center_y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5

        if distance < (player_width // 2 + point_radius):
            player_score += 1
            print("Player Score:", player_score)  # Adicionando print para depuração
            points_since_last_weapon += 1
            if points_since_last_weapon >= 50:
                has_weapon = True
                points_since_last_weapon = 0
            if player_score % 50 == 0:
                player_lives += 1  # Adicionando uma vida a cada 50 pontos
            if player_score % 100 == 0:
                player_level += 1
        else:
            new_points.append(point)
    points.clear()
    points.extend(new_points)

# Função para verificar colisões entre os projéteis e os inimigos
def check_collisions_with_projectiles():
    global enemies, projectiles

    new_enemies = []
    new_projectiles = []
    for projectile in projectiles:
        projectile_center_x = projectile[0]
        projectile_center_y = projectile[1]

        for enemy in enemies:
            enemy_center_x = enemy[0] + enemy_width // 2
            enemy_center_y = enemy[1] + enemy_height // 2

            dx = projectile_center_x - enemy_center_x
            dy = projectile_center_y - enemy_center_y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance < (projectile_radius + enemy_width // 2):
                # Remover inimigo atingido
                enemies.remove(enemy)
                break
        else:
            new_projectiles.append(projectile)

    enemies.clear()
    enemies.extend(new_enemies)
    projectiles.clear()
    projectiles.extend(new_projectiles)

# Função para atualizar o estado de invencibilidade do jogador após colisão
def update_invincibility():
    global is_invincible, invincible_timer
    if is_invincible:
        invincible_timer -= get_delta_time()
        if invincible_timer <= 0:
            is_invincible = False

# Função para atirar projéteis
def shoot():
    global projectiles
    if has_weapon:
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - player_center_y, mouse_x - player_center_x)
        projectile_dx = math.cos(angle) * projectile_speed
        projectile_dy = math.sin(angle) * projectile_speed
        projectiles.append([player_center_x, player_center_y, projectile_dx, projectile_dy])

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gerar novos inimigos a cada 7 segundos após a morte de todos os inimigos
    if len(enemies) == 0:
        enemy_respawn_timer += get_delta_time()
        if enemy_respawn_timer >= enemy_respawn_time:
            enemy_respawn_timer = 0
            current_enemies = enemies_per_level * player_level
            spawn_enemies()  # Gerar novos inimigos

    # Verificar colisões entre jogador e inimigos
    check_collisions_with_enemies()

    # Gerar novos pontos verdes a cada 2 segundos
    points_spawn_interval -= get_delta_time()
    if points_spawn_interval <= 0:
        points_spawn_interval = 2.0  # Reiniciar o intervalo de 2 segundos
        spawn_point()

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed

    # Atirar projéteis se o jogador tiver a arma e pressionar o botão do mouse
    if has_weapon and pygame.mouse.get_pressed()[0]:
        shoot()

    # Movimentação dos inimigos em direção ao jogador
    delta_time = get_delta_time()
    for idx, enemy in enumerate(enemies):
        dx = player_x - enemy[0]
        dy = player_y - enemy[1]
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance
            enemies[idx][0] += direction_x * enemy_speed * delta_time
            enemies[idx][1] += direction_y * enemy_speed * delta_time

    # Verificar colisões entre jogador e inimigos
    check_collisions_with_enemies()

    # Verificar colisões entre jogador e pontos verdes
    check_collisions_with_points()

    # Verificar colisões entre projéteis e inimigos
    check_collisions_with_projectiles()

    # Atualizar estado de invencibilidade do jogador
    update_invincibility()

    # Limpar a tela
    screen.fill(BLACK)

    # Desenhar o timer na tela
    font_timer = pygame.font.SysFont(None, 30)
    timer_text = f"Próximo inimigo em: {int(enemy_respawn_time - enemy_respawn_timer)}s"
    timer_surface = font_timer.render(timer_text, True, WHITE)
    screen.blit(timer_surface, (10, 10))

    # Desenhar a quantidade de inimigos restantes na tela
    font_enemies = pygame.font.SysFont(None, 30)
    enemies_text = f"Inimigos restantes: {current_enemies}"
    enemies_surface = font_enemies.render(enemies_text, True, WHITE)
    screen.blit(enemies_surface, (10, 40))

    # Desenhar o jogador
    if not is_invincible or int(invincible_timer * 10) % 2 == 0:
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Desenhar os inimigos
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

    # Desenhar os pontos verdes
    for point in points:
        pygame.draw.circle(screen, GREEN, (point[0] + point_radius, point[1] + point_radius), point_radius)

    # Desenhar os projéteis
    for projectile in projectiles:
        pygame.draw.circle(screen, WHITE, (int(projectile[0]), int(projectile[1])), projectile_radius)

    # Exibir informações do jogador na tela
    font = pygame.font.SysFont(None, 24)
    score_text = font.render("Pontos: " + str(player_score), True, WHITE)
    lives_text = font.render("Vidas: " + str(player_lives), True, WHITE)
    level_text = font.render("Nível: " + str(player_level), True, WHITE)
    weapon_text = font.render("Arma: " + ("Sim" if has_weapon else "Não"), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (10, 70))
    screen.blit(weapon_text, (10, 100))

    # Atualizar a tela
    pygame.display.flip()

    # Controlar o FPS (60 FPS)
    clock.tick(60)
