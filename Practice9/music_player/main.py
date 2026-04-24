import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 700, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 22)

player = MusicPlayer("music_player/music")

def draw(text, font, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

running = True

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.back()
            elif event.key == pygame.K_q:
                running = False

    draw("Music Player", font, 240, 30)

    draw("Track:", small_font, 50, 120)
    draw(player.get_track_name(), small_font, 50, 150)

    status = "Playing" if player.is_playing else "Stopped"
    draw("Status: " + status, small_font, 50, 200)

    pos = player.get_position()
    draw("Position: " + str(pos) + " sec", small_font, 50, 230)

    pygame.draw.rect(screen, (100, 100, 100), (50, 280, 600, 20))
    w = pos * 5
    if w > 600:
        w = 600
    pygame.draw.rect(screen, (0, 200, 100), (50, 280, w, 20))

    draw("P Play | S Stop | N Next | B Back | Q Quit", small_font, 50, 330)

    pygame.display.update()

pygame.quit()