import pygame
import random
from datetime import datetime
from persistence import load_json, save_json

WIDTH = 500
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (45, 45, 45)
RED = (220, 40, 40)
GREEN = (40, 200, 40)
BLUE = (40, 120, 255)
YELLOW = (240, 220, 40)
ORANGE = (255, 140, 0)
PURPLE = (160, 60, 220)
CYAN = (0, 220, 220)

LEADERBOARD_FILE = "leaderboard.json"


def get_color(name):
    if name == "red":
        return RED
    if name == "green":
        return GREEN
    if name == "yellow":
        return YELLOW
    return BLUE


class Player:
    def __init__(self, color):
        self.rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 90, 40, 60)
        self.color = color
        self.shield = False
        self.active_power = None
        self.power_end = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 70:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 70:
            self.rect.x += 6
        if keys[pygame.K_UP] and self.rect.top > 80:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT - 20:
            self.rect.y += 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        if self.shield:
            pygame.draw.circle(screen, CYAN, self.rect.center, 38, 3)


class FallingObject:
    def __init__(self, kind, speed, player_rect):
        self.kind = kind
        self.speed = speed
        self.timeout = pygame.time.get_ticks() + 6000
        self.weight = 1

        if kind == "enemy":
            self.rect = pygame.Rect(0, -80, 40, 60)
            self.color = RED
        elif kind == "coin":
            self.rect = pygame.Rect(0, -30, 25, 25)
            self.color = YELLOW
            self.weight = random.choice([1, 2, 3])
        elif kind == "oil":
            self.rect = pygame.Rect(0, -30, 50, 25)
            self.color = BLACK
        elif kind == "barrier":
            self.rect = pygame.Rect(0, -30, 70, 25)
            self.color = ORANGE
        elif kind == "nitro":
            self.rect = pygame.Rect(0, -30, 35, 35)
            self.color = PURPLE
        elif kind == "shield":
            self.rect = pygame.Rect(0, -30, 35, 35)
            self.color = CYAN
        else:
            self.rect = pygame.Rect(0, -30, 35, 35)
            self.color = GREEN

        self.safe_spawn(player_rect)

    def safe_spawn(self, player_rect):
        while True:
            lane_x = random.choice([105, 180, 255, 330])
            self.rect.centerx = lane_x
            self.rect.y = random.randint(-260, -40)

            if abs(self.rect.centerx - player_rect.centerx) > 60 or player_rect.y < 400:
                break

    def move(self, bonus=0):
        self.rect.y += self.speed + bonus

    def draw(self, screen, small_font):
        if self.kind == "coin":
            pygame.draw.circle(screen, self.color, self.rect.center, 13)
            text = small_font.render(str(self.weight), True, BLACK)
            screen.blit(text, (self.rect.x + 8, self.rect.y + 2))

        elif self.kind == "oil":
            pygame.draw.ellipse(screen, self.color, self.rect)

        elif self.kind == "barrier":
            pygame.draw.rect(screen, self.color, self.rect)

        elif self.kind == "nitro":
            pygame.draw.rect(screen, self.color, self.rect)
            text = small_font.render("N", True, WHITE)
            screen.blit(text, (self.rect.x + 10, self.rect.y + 5))

        elif self.kind == "shield":
            pygame.draw.circle(screen, self.color, self.rect.center, 18)
            text = small_font.render("S", True, BLACK)
            screen.blit(text, (self.rect.x + 11, self.rect.y + 5))

        elif self.kind == "repair":
            pygame.draw.rect(screen, self.color, self.rect)
            text = small_font.render("+", True, BLACK)
            screen.blit(text, (self.rect.x + 10, self.rect.y + 5))

        else:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)


class Game:
    def __init__(self, screen, clock, username, settings, small_font):
        self.screen = screen
        self.clock = clock
        self.username = username
        self.settings = settings
        self.small_font = small_font

        self.player = Player(get_color(settings["car_color"]))

        self.objects = []
        self.score = 0
        self.coins = 0
        self.distance = 0
        self.finish_distance = 5000

        if settings["difficulty"] == "easy":
            self.base_speed = 4
            self.spawn_rate = 50
        elif settings["difficulty"] == "hard":
            self.base_speed = 7
            self.spawn_rate = 28
        else:
            self.base_speed = 5
            self.spawn_rate = 38

        self.speed = self.base_speed
        self.frame = 0
        self.running = True

    def spawn_objects(self):
        self.frame += 1

        difficulty_bonus = self.distance // 700
        rate = max(12, self.spawn_rate - difficulty_bonus * 3)

        if self.frame % rate == 0:
            kind = random.choice(["enemy", "enemy", "coin", "coin", "oil", "barrier"])
            self.objects.append(FallingObject(kind, self.speed, self.player.rect))

        if self.frame % 250 == 0:
            kind = random.choice(["nitro", "shield", "repair"])
            self.objects.append(FallingObject(kind, self.speed, self.player.rect))

    def apply_powerup(self, kind):
        now = pygame.time.get_ticks()

        if self.player.active_power is not None:
            return

        if kind == "nitro":
            self.player.active_power = "Nitro"
            self.player.power_end = now + 4000

        elif kind == "shield":
            self.player.active_power = "Shield"
            self.player.shield = True

        elif kind == "repair":
            self.objects = [obj for obj in self.objects if obj.kind not in ["enemy", "oil", "barrier"]]
            self.score += 10

    def update_powerups(self):
        now = pygame.time.get_ticks()

        if self.player.active_power == "Nitro":
            self.speed = self.base_speed + 5

            if now > self.player.power_end:
                self.speed = self.base_speed
                self.player.active_power = None

        else:
            self.speed = self.base_speed

    def handle_collision(self, obj):
        if obj.kind in ["enemy", "barrier"]:
            if self.player.shield:
                self.player.shield = False
                self.player.active_power = None
                self.objects.remove(obj)
            else:
                self.running = False

        elif obj.kind == "oil":
            self.base_speed = max(3, self.base_speed - 1)
            self.objects.remove(obj)

        elif obj.kind == "coin":
            self.coins += obj.weight
            self.score += obj.weight * 10
            self.objects.remove(obj)

            if self.coins % 5 == 0:
                self.base_speed += 1

        elif obj.kind in ["nitro", "shield", "repair"]:
            self.apply_powerup(obj.kind)
            self.objects.remove(obj)

    def save_score(self):
        data = load_json(LEADERBOARD_FILE, [])

        data.append({
            "name": self.username,
            "score": self.score,
            "distance": self.distance,
            "coins": self.coins,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
        save_json(LEADERBOARD_FILE, data)

    def draw_road(self):
        self.screen.fill((20, 120, 20))
        pygame.draw.rect(self.screen, ROAD, (60, 0, WIDTH - 120, HEIGHT))

        for x in [145, 225, 305]:
            for y in range(-80, HEIGHT, 80):
                pygame.draw.rect(self.screen, WHITE, (x, y + (self.distance % 80), 5, 40))

    def draw_hud(self):
        remaining = max(0, self.finish_distance - self.distance)

        texts = [
            "Score: " + str(self.score),
            "Coins: " + str(self.coins),
            "Distance: " + str(self.distance),
            "Left: " + str(remaining)
        ]

        y = 10
        for text in texts:
            img = self.small_font.render(text, True, WHITE)
            self.screen.blit(img, (10, y))
            y += 20

        if self.player.active_power == "Nitro":
            left = max(0, (self.player.power_end - pygame.time.get_ticks()) // 1000)
            power_text = "Power: Nitro " + str(left)
        elif self.player.active_power == "Shield":
            power_text = "Power: Shield"
        else:
            power_text = "Power: none"

        img = self.small_font.render(power_text, True, WHITE)
        self.screen.blit(img, (320, 10))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_score()
                    pygame.quit()
                    raise SystemExit

            self.player.move()
            self.update_powerups()
            self.spawn_objects()

            self.distance += 1
            self.score += 1

            for obj in self.objects[:]:
                obj.move()

                if obj.rect.top > HEIGHT:
                    self.objects.remove(obj)

                elif obj.kind in ["nitro", "shield", "repair"] and pygame.time.get_ticks() > obj.timeout:
                    self.objects.remove(obj)

                elif obj.rect.colliderect(self.player.rect):
                    self.handle_collision(obj)

            if self.distance >= self.finish_distance:
                self.running = False

            self.draw_road()

            for obj in self.objects:
                obj.draw(self.screen, self.small_font)

            self.player.draw(self.screen)
            self.draw_hud()

            pygame.display.update()
            self.clock.tick(FPS)

        self.save_score()
        return self.score, self.distance, self.coins