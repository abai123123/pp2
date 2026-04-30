import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

background = pygame.image.load("mainclock.png").convert()
right_hand = pygame.image.load("rightarm.png").convert_alpha()
left_hand = pygame.image.load("leftarm.png").convert_alpha()

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
right_hand = pygame.transform.scale(right_hand, (250, 250))
left_hand = pygame.transform.scale(left_hand, (250, 250))

center = (WIDTH // 2, HEIGHT // 2)

def rotate_hand(image, angle, pivot, hand_start):
    rotated = pygame.transform.rotate(image, angle)

    image_center = pygame.math.Vector2(
        image.get_width() / 2,
        image.get_height() / 2
    )

    hand_start = pygame.math.Vector2(hand_start)

    offset = image_center - hand_start
    rotated_offset = offset.rotate(-angle)

    rect = rotated.get_rect(
        center=(pivot[0] + rotated_offset.x, pivot[1] + rotated_offset.y)
    )

    return rotated, rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second
    micro = now.microsecond

    minute_angle = 90 - (minutes + seconds / 60) * 6
    second_angle = 90 - (seconds + micro / 1000000) * 6

    screen.blit(background, (0, 0))

    right_start = (230, 10)
    left_start = (0, 0)

    right_rot, right_rect = rotate_hand(right_hand, minute_angle, center, right_start)
    left_rot, left_rect = rotate_hand(left_hand, second_angle, center, left_start)

    screen.blit(right_rot, right_rect)
    screen.blit(left_rot, left_rect)

    pygame.display.update()
    clock.tick(120)

pygame.quit()