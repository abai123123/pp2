import pygame
import sys
from persistence import load_json, save_json

WIDTH = 500
HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
YELLOW = (240, 220, 40)
RED = (220, 40, 40)

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def draw_text(screen, text, x, y, color, font):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_button(screen, text, rect, font):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    image = font.render(text, True, WHITE)
    screen.blit(image, (rect.x + 20, rect.y + 12))


def username_screen(screen, font, small_font):
    name = ""

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Enter username:", 100, 230, WHITE, font)
        draw_text(screen, name + "|", 100, 270, YELLOW, font)
        draw_text(screen, "Press Enter to start", 100, 330, WHITE, small_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode


def leaderboard_screen(screen, font, small_font):
    data = load_json(LEADERBOARD_FILE, [])

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Leaderboard Top 10", 90, 40, YELLOW, font)

        y = 100

        for i, entry in enumerate(data):
            line = str(i + 1) + ". " + entry["name"] + " | Score: " + str(entry["score"]) + " | Dist: " + str(entry["distance"])
            draw_text(screen, line, 30, y, WHITE, small_font)
            y += 35

        draw_text(screen, "Press ESC to go back", 130, 640, WHITE, small_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


def settings_screen(screen, settings, font, small_font, big_font):
    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(BLACK)

        draw_text(screen, "Settings", 160, 60, YELLOW, big_font)

        draw_text(screen, "1. Sound: " + str(settings["sound"]), 90, 160, WHITE, font)
        draw_text(screen, "2. Car Color: " + settings["car_color"], 90, 210, WHITE, font)
        draw_text(screen, "3. Difficulty: " + settings["difficulty"], 90, 260, WHITE, font)

        draw_text(screen, "Press 1/2/3 to change", 90, 340, WHITE, small_font)
        draw_text(screen, "ESC - Back and Save", 90, 370, WHITE, small_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_json(SETTINGS_FILE, settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_json(SETTINGS_FILE, settings)
                    return

                if event.key == pygame.K_1:
                    settings["sound"] = not settings["sound"]

                elif event.key == pygame.K_2:
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]

                elif event.key == pygame.K_3:
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]


def game_over_screen(screen, score, distance, coins, font, big_font):
    retry = pygame.Rect(140, 330, 220, 50)
    menu = pygame.Rect(140, 400, 220, 50)

    while True:
        screen.fill(BLACK)

        draw_text(screen, "GAME OVER", 115, 120, RED, big_font)
        draw_text(screen, "Score: " + str(score), 150, 200, WHITE, font)
        draw_text(screen, "Distance: " + str(distance), 150, 235, WHITE, font)
        draw_text(screen, "Coins: " + str(coins), 150, 270, WHITE, font)

        draw_button(screen, "Retry", retry, font)
        draw_button(screen, "Main Menu", menu, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(event.pos):
                    return "retry"
                if menu.collidepoint(event.pos):
                    return "menu"