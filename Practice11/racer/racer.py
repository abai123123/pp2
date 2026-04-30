import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COIN = 0

# После каждых N монет скорость врага увеличивается
N = 5

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Двигаем врага вниз
        self.rect.move_ip(0, SPEED)

        # Если враг ушёл вниз за экран, возвращаем наверх
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загружаем картинку монетки
        self.image = pygame.image.load("Coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()

        # Вес монетки: 1, 2 или 3
        self.weight = random.choice([1, 2, 3])

        self.generate()

    def generate(self):
        # Случайная позиция монетки на дороге
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        # Каждый раз новая стоимость монетки
        self.weight = random.choice([1, 2, 3])

    def move(self):
        # Монетка падает вниз
        self.rect.move_ip(0, SPEED)

        # Если монетка ушла за экран, создаём новую
        if self.rect.top > SCREEN_HEIGHT:
            self.generate()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Движение влево
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Движение вправо
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))

    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render("Coins: " + str(COIN), True, BLACK)
    DISPLAYSURF.blit(coins_text, (10, 35))

    speed_text = font_small.render("Speed: " + str(SPEED), True, BLACK)
    DISPLAYSURF.blit(speed_text, (10, 60))

    weight_text = font_small.render("Coin value: " + str(C1.weight), True, BLACK)
    DISPLAYSURF.blit(weight_text, (10, 85))

    # Двигаем и рисуем все объекты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка столкновения игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка столкновения игрока с монеткой
    if pygame.sprite.spritecollideany(P1, coins):
        old_coin = COIN

        # Добавляем не 1, а вес монетки
        COIN += C1.weight

        pygame.mixer.Sound("coins.wav").play()

        # Если игрок собрал N монет, увеличиваем скорость
        if COIN // N > old_coin // N:
            SPEED += 1

        # Создаём новую монетку
        C1.generate()

    pygame.display.update()
    FramePerSec.tick(FPS)