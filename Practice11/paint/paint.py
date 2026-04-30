import pygame
import math

def main():
    pygame.init()

    WIDTH = 900
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 15
    mode = "pen"
    color = (0, 0, 255)
    drawing = False
    start_pos = None

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))

    font = pygame.font.SysFont("Verdana", 14)

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_p:
                    mode = "pen"
                elif event.key == pygame.K_r:
                    mode = "rectangle"
                elif event.key == pygame.K_c:
                    mode = "circle"
                elif event.key == pygame.K_e:
                    mode = "eraser"
                elif event.key == pygame.K_s:
                    mode = "square"
                elif event.key == pygame.K_t:
                    mode = "right_triangle"
                elif event.key == pygame.K_u:
                    mode = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    mode = "rhombus"

                elif event.key == pygame.K_1:
                    color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)
                elif event.key == pygame.K_4:
                    color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos

                    if mode == "pen":
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    elif mode == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 4:
                    radius = min(100, radius + 1)

                elif event.button == 5:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos is not None:
                    end_pos = event.pos
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    if mode == "rectangle":
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        pygame.draw.rect(canvas, color, (x, y, w, h), radius)

                    elif mode == "square":
                        size = min(abs(x2 - x1), abs(y2 - y1))

                        if x2 < x1:
                            x = x1 - size
                        else:
                            x = x1

                        if y2 < y1:
                            y = y1 - size
                        else:
                            y = y1

                        pygame.draw.rect(canvas, color, (x, y, size, size), radius)

                    elif mode == "circle":
                        dx = x2 - x1
                        dy = y2 - y1
                        r = int((dx * dx + dy * dy) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, radius)

                    elif mode == "right_triangle":
                        points = [(x1, y1), (x2, y1), (x1, y2)]
                        pygame.draw.polygon(canvas, color, points, radius)

                    elif mode == "equilateral_triangle":
                        side = abs(x2 - x1)
                        h = int(side * math.sqrt(3) / 2)

                        if x2 >= x1:
                            points = [
                                (x1, y1),
                                (x1 + side, y1),
                                (x1 + side // 2, y1 - h)
                            ]
                        else:
                            points = [
                                (x1, y1),
                                (x1 - side, y1),
                                (x1 - side // 2, y1 - h)
                            ]

                        pygame.draw.polygon(canvas, color, points, radius)

                    elif mode == "rhombus":
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        dx = abs(x2 - x1) // 2
                        dy = abs(y2 - y1) // 2

                        points = [
                            (cx, cy - dy),
                            (cx + dx, cy),
                            (cx, cy + dy),
                            (cx - dx, cy)
                        ]

                        pygame.draw.polygon(canvas, color, points, radius)

                    drawing = False
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == "pen":
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    elif mode == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

        screen.blit(canvas, (0, 0))

        info1 = "Mode: " + mode + " | Size: " + str(radius)
        info2 = "P pen | R rect | S square | C circle | T right triangle | U equilateral | H rhombus | E eraser"
        info3 = "Colors: 1 red | 2 green | 3 blue | 4 white | Mouse wheel size | Right click smaller"

        text1 = font.render(info1, True, (255, 255, 255))
        text2 = font.render(info2, True, (255, 255, 255))
        text3 = font.render(info3, True, (255, 255, 255))

        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))
        screen.blit(text3, (10, 50))

        pygame.display.flip()
        clock.tick(60)

main()