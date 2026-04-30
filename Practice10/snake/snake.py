import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 10
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCORE = 0
LEVEL = 1
FOODS_FOR_LEVEL = 3

font = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


class Snake:
    def __init__(self):
        # Snake body parts. First element is the head.
        self.body = [(300, 300), (280, 300), (260, 300)]

        # Starting direction
        self.direction = "RIGHT"

        # New direction from keyboard
        self.change_to = self.direction

    def change_direction(self):
        # Snake cannot turn directly opposite
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self):
        # Get current head position
        x, y = self.body[0]

        # Move head by one cell
        if self.direction == "UP":
            y -= CELL_SIZE
        if self.direction == "DOWN":
            y += CELL_SIZE
        if self.direction == "LEFT":
            x -= CELL_SIZE
        if self.direction == "RIGHT":
            x += CELL_SIZE

        # Add new head to the beginning
        new_head = (x, y)
        self.body.insert(0, new_head)

    def remove_tail(self):
        # Remove last part if food was not eaten
        self.body.pop()

    def draw(self, surface):
        # Draw every part of snake
        for block in self.body:
            pygame.draw.rect(surface, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

    def wall_collision(self):
        # Check if snake leaves the screen
        x, y = self.body[0]

        if x < 0 or x >= SCREEN_WIDTH:
            return True
        if y < 0 or y >= SCREEN_HEIGHT:
            return True

        return False

    def self_collision(self):
        # Check if head touches body
        head = self.body[0]

        if head in self.body[1:]:
            return True

        return False


class Food:
    def __init__(self, snake_body):
        # Generate first food position
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            # Random cell position
            x = random.randrange(0, SCREEN_WIDTH, CELL_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, CELL_SIZE)

            # Food must not appear on snake
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, surface):
        # Draw food
        pygame.draw.rect(surface, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


def game_over():
    DISPLAYSURF.fill(BLACK)

    text = font_big.render("Game Over", True, RED)
    DISPLAYSURF.blit(text, (120, 250))

    pygame.display.update()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()


snake = Snake()
food = Food(snake.body)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                snake.change_to = "UP"
            if event.key == K_DOWN:
                snake.change_to = "DOWN"
            if event.key == K_LEFT:
                snake.change_to = "LEFT"
            if event.key == K_RIGHT:
                snake.change_to = "RIGHT"

    snake.change_direction()
    snake.move()

    # Check wall collision
    if snake.wall_collision():
        game_over()

    # Check self collision
    if snake.self_collision():
        game_over()

    # Check food collision
    if snake.body[0] == food.position:
        SCORE += 1

        # Generate new food not on snake
        food.position = food.generate_position(snake.body)

        # Increase level every 3 foods
        if SCORE % FOODS_FOR_LEVEL == 0:
            LEVEL += 1
            FPS += 2

    else:
        # If food was not eaten, snake does not grow
        snake.remove_tail()

    DISPLAYSURF.fill(BLACK)

    snake.draw(DISPLAYSURF)
    food.draw(DISPLAYSURF)

    score_text = font.render("Score: " + str(SCORE), True, WHITE)
    level_text = font.render("Level: " + str(LEVEL), True, WHITE)

    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(level_text, (10, 35))

    pygame.display.update()
    FramePerSec.tick(FPS)