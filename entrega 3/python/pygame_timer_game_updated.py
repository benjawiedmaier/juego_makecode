import pygame
import random
import sys

# Inicialización
pygame.init()
WIDTH, HEIGHT = 480, 320
SCALE = 1
SCREEN = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)

# Cargar imágenes
bg_start = pygame.image.load("pizzeria.png")
bg_game = pygame.image.load("roads2.png")
player_img_original = pygame.image.load("player.png")
pizza_img = pygame.image.load("pizza_piece.png")

# Escalar imágenes
bg_start = pygame.transform.scale(bg_start, (WIDTH, HEIGHT))
bg_game = pygame.transform.scale(bg_game, (WIDTH, HEIGHT))
player_img_small = pygame.transform.scale(player_img_original, (64, 64))
player_img_large = pygame.transform.scale(player_img_original, (64, 64))
pizza_img = pygame.transform.scale(pizza_img, (64, 64))

# Clases
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

# Variables globales
score = 0
base_speed = 7
boost_speed = 40
Xvel = base_speed
Yvel = base_speed
TIMER_DURATION = 3000
last_pizza_time = pygame.time.get_ticks()
boost_active = False
boost_start_time = 0
boost_cooldown_start = -5000
boost_duration = 1000
boost_cooldown = 5000

player = Sprite(player_img_large, 61, 101)
pizza = Sprite(pizza_img, random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))
sprites = pygame.sprite.Group()
sprites.add(player, pizza)

def splash_screen():
    player.image = player_img_large
    player.rect = player.image.get_rect(center=(WIDTH // 3, HEIGHT // 10 * 9 + 5))
    waiting = True
    while waiting:
        SCREEN.blit(pygame.transform.scale(bg_start, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        SCREEN.blit(pygame.transform.scale(player.image, (64 * SCALE // 4 * 6 , 64 * SCALE // 4 * 6)),
                    (player.rect.x * SCALE, player.rect.y * SCALE - 50))

        bar_width = WIDTH * SCALE
        bar_height = 50
        bar_y = HEIGHT * SCALE // 2 - bar_height // 2
        pygame.draw.rect(SCREEN, (0, 0, 0), (0, bar_y, bar_width, bar_height))

        text = FONT.render("Game Start!", True, (255, 255, 255))
        SCREEN.blit(text, (bar_width // 2 - text.get_width() // 2, bar_y + 5))

        inst_text = FONT.render("Press A to start", True, (255, 255, 255))
        SCREEN.blit(inst_text, (bar_width - inst_text.get_width() - 10, bar_y + bar_height - inst_text.get_height() - 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            waiting = False

def draw_game(time_left):
    SCREEN.blit(pygame.transform.scale(bg_game, (WIDTH * SCALE , HEIGHT * SCALE )), (0, 0))
    for sprite in sprites:
        SCREEN.blit(pygame.transform.scale(sprite.image, (16 * SCALE * 3, 16 * SCALE*3)),
                    (sprite.rect.x * SCALE, sprite.rect.y * SCALE))
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))

    time_rect = pygame.Rect(WIDTH * SCALE - 90, 10, 80, 30)
    pygame.draw.rect(SCREEN, (0, 0, 0), time_rect)
    time_text = FONT.render(f"Time: {round(time_left, 1)}", True, (255, 255, 255))
    SCREEN.blit(time_text, (WIDTH * SCALE - time_text.get_width() - 15, 15))
    pygame.display.flip()

def game_over():
    splash_screen()

def reset_game():
    global score, Xvel, Yvel, last_pizza_time, boost_active, boost_start_time, boost_cooldown_start
    player.image = player_img_small
    player.rect = player.image.get_rect(center=(61, 101))
    pizza.rect.topleft = (random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))
    Xvel = base_speed
    Yvel = base_speed
    score = 0
    last_pizza_time = pygame.time.get_ticks()
    boost_active = False
    boost_start_time = 0
    boost_cooldown_start = -5000

splash_screen()
reset_game()
running = True
while running:
    CLOCK.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.vx = player.vy = 0
    if keys[pygame.K_w]:
        player.vy = -Yvel
    if keys[pygame.K_s]:
        player.vy = Yvel
    if keys[pygame.K_a]:
        player.vx = -Xvel
    if keys[pygame.K_d]:
        player.vx = Xvel

    current_time = pygame.time.get_ticks()

    if keys[pygame.K_e] and not boost_active and current_time - boost_cooldown_start >= boost_cooldown:
        boost_active = True
        boost_start_time = current_time
        Xvel = boost_speed
        Yvel = boost_speed

    if boost_active and current_time - boost_start_time > boost_duration:
        boost_active = False
        boost_cooldown_start = current_time
        Xvel = base_speed
        Yvel = base_speed

    if keys[pygame.K_r]:
        splash_screen()
        reset_game()

    player.update()

    time_left = max(0, (TIMER_DURATION - (current_time - last_pizza_time)) / 1000)

    if pygame.sprite.collide_rect(player, pizza):
        score += 1
        last_pizza_time = current_time
        pizza.rect.topleft = (random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))

    if time_left <= 0:
        game_over()
        reset_game()

    draw_game(time_left)

pygame.quit()
sys.exit()
