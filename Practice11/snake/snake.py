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
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

SCORE = 0
LEVEL = 1
FOODS_FOR_LEVEL = 5

FOOD_LIFETIME = 4000

font = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")


class Snake:
    def __init__(self):
        # Body of the snake. First element is the head.
        self.body = [(300, 300), (280, 300), (260, 300)]

        # Current moving direction
        self.direction = "RIGHT"

        # Direction selected by keyboard
        self.change_to = self.direction

    def change_direction(self):
        # Snake cannot move directly backwards
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self):
        # Take current head coordinates
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

        # Add new head
        self.body.insert(0, (x, y))

    def remove_tail(self):
        # Remove tail if food was not eaten
        self.body.pop()

    def grow(self, amount):
        # Add extra body parts depending on food weight
        tail = self.body[-1]

        for i in range(amount - 1):
            self.body.append(tail)

    def draw(self, surface):
        # Draw snake blocks
        for block in self.body:
            pygame.draw.rect(surface, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

    def wall_collision(self):
        # Check collision with screen borders
        x, y = self.body[0]

        if x < 0 or x >= SCREEN_WIDTH:
            return True
        if y < 0 or y >= SCREEN_HEIGHT:
            return True

        return False

    def self_collision(self):
        # Check collision with snake body
        head = self.body[0]

        if head in self.body[1:]:
            return True

        return False


class Food:
    def __init__(self, snake_body):
        # Generate first food
        self.position = (0, 0)
        self.weight = 1
        self.spawn_time = 0
        self.generate(snake_body)

    def generate_position(self, snake_body):
        while True:
            # Random position by grid
            x = random.randrange(0, SCREEN_WIDTH, CELL_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, CELL_SIZE)

            # Food must not spawn on snake
            if (x, y) not in snake_body:
                return (x, y)

    def generate(self, snake_body):
        # Generate new position
        self.position = self.generate_position(snake_body)

        # Random food weight
        self.weight = random.choice([1, 2, 3])

        # Save time when food appeared
        self.spawn_time = pygame.time.get_ticks()

    def expired(self):
        # Check if food existed longer than FOOD_LIFETIME
        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time > FOOD_LIFETIME:
            return True

        return False

    def draw(self, surface):
        # Food color depends on weight
        if self.weight == 1:
            color = RED
        elif self.weight == 2:
            color = YELLOW
        else:
            color = BLUE

        pygame.draw.rect(surface, color, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


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

    # If food disappeared by timer, generate new food
    if food.expired():
        food.generate(snake.body)

    # Check food collision
    if snake.body[0] == food.position:
        SCORE += food.weight

        # Snake grows depending on food weight
        snake.grow(food.weight)

        # Generate new food after eating
        food.generate(snake.body)

        # Increase level depending on score
        if SCORE >= LEVEL * FOODS_FOR_LEVEL:
            LEVEL += 1
            FPS += 2

    else:
        # If food was not eaten, snake moves normally
        snake.remove_tail()

    DISPLAYSURF.fill(BLACK)

    snake.draw(DISPLAYSURF)
    food.draw(DISPLAYSURF)

    score_text = font.render("Score: " + str(SCORE), True, WHITE)
    level_text = font.render("Level: " + str(LEVEL), True, WHITE)
    weight_text = font.render("Food: " + str(food.weight), True, WHITE)

    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(level_text, (10, 35))
    DISPLAYSURF.blit(weight_text, (10, 60))

    pygame.display.update()
    FramePerSec.tick(FPS)