
import pygame
import random
import sys

# Inicialización
pygame.init()
WIDTH, HEIGHT = 160, 120
SCALE = 4
SCREEN = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)

# Cargar imágenes
bg_start = pygame.image.load("pizzeria.png")
bg_game = pygame.image.load("roads.png")
player_img = pygame.image.load("player.png")
pizza_img = pygame.image.load("pizza_piece.png")

# Escalar imágenes
bg_start = pygame.transform.scale(bg_start, (WIDTH, HEIGHT))
bg_game = pygame.transform.scale(bg_game, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (16, 16))
pizza_img = pygame.transform.scale(pizza_img, (16, 16))

# Clases
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

# Variables globales
score = 0
Xvel = 80 // 10
Yvel = 80 // 10

player = Sprite(player_img, 61, 101)
pizza = Sprite(pizza_img, random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))
sprites = pygame.sprite.Group()
sprites.add(player, pizza)

def splash_screen():
    SCREEN.blit(pygame.transform.scale(bg_start, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    text = FONT.render("Game Start!", True, (255, 255, 255))
    SCREEN.blit(text, (WIDTH * SCALE // 2 - text.get_width() // 2, HEIGHT * SCALE // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_game():
    SCREEN.blit(pygame.transform.scale(bg_game, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    for sprite in sprites:
        SCREEN.blit(pygame.transform.scale(sprite.image, (16 * SCALE, 16 * SCALE)),
                    (sprite.rect.x * SCALE, sprite.rect.y * SCALE))
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))
    pygame.display.flip()

def reset_game():
    global score, Xvel, Yvel
    player.rect.center = (61, 101)
    pizza.rect.topleft = (random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))
    Xvel = 80 // 10
    Yvel = 80 // 10
    score = 0

splash_screen()
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
    if keys[pygame.K_q]:  # botón A
        Xvel = 100 // 10
        Yvel = 100 // 10
    if keys[pygame.K_t]:  # reset
        reset_game()
    if keys[pygame.K_r]:  # menú
        splash_screen()

    player.update()

    if pygame.sprite.collide_rect(player, pizza):
        score += 1
        pizza.rect.topleft = (random.randint(0, WIDTH - 16), random.randint(0, HEIGHT - 16))

    draw_game()

pygame.quit()
sys.exit()
