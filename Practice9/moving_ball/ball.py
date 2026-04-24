import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.step = 20

    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x - self.radius < 0:
            return
        if new_x + self.radius > width:
            return
        if new_y - self.radius < 0:
            return
        if new_y + self.radius > height:
            return

        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)