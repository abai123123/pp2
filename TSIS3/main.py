import pygame
import sys

from persistence import load_json, save_json
from racer import Game
from ui import username_screen, leaderboard_screen, settings_screen, game_over_screen, draw_text, draw_button

pygame.init()

WIDTH = 500
HEIGHT = 700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (240, 220, 40)

SETTINGS_FILE = "settings.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 40)


def default_settings():
    return {
        "sound": True,
        "car_color": "blue",
        "difficulty": "normal"
    }


def main_menu():
    settings = load_json(SETTINGS_FILE, default_settings())

    play_btn = pygame.Rect(150, 180, 200, 50)
    board_btn = pygame.Rect(150, 250, 200, 50)
    settings_btn = pygame.Rect(150, 320, 200, 50)
    quit_btn = pygame.Rect(150, 390, 200, 50)

    while True:
        screen.fill(BLACK)

        draw_text(screen, "TSIS3 RACER", 105, 80, YELLOW, big_font)

        draw_button(screen, "Play", play_btn, font)
        draw_button(screen, "Leaderboard", board_btn, font)
        draw_button(screen, "Settings", settings_btn, font)
        draw_button(screen, "Quit", quit_btn, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_json(SETTINGS_FILE, settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    username = username_screen(screen, font, small_font)

                    while True:
                        game = Game(screen, clock, username, settings, small_font)
                        score, distance, coins = game.run()

                        choice = game_over_screen(screen, score, distance, coins, font, big_font)

                        if choice == "retry":
                            continue

                        if choice == "menu":
                            break

                elif board_btn.collidepoint(event.pos):
                    leaderboard_screen(screen, font, small_font)

                elif settings_btn.collidepoint(event.pos):
                    settings_screen(screen, settings, font, small_font, big_font)

                elif quit_btn.collidepoint(event.pos):
                    save_json(SETTINGS_FILE, settings)
                    pygame.quit()
                    sys.exit()


main_menu()