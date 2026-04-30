import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 15
    mode = "pen"
    color = (0, 0, 255)
    drawing = False
    start_pos = None

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

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

                    if mode == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 4:
                    radius = min(100, radius + 1)

                elif event.button == 5:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    end_pos = event.pos

                    if mode == "rectangle":
                        x1, y1 = start_pos
                        x2, y2 = end_pos

                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)

                        pygame.draw.rect(canvas, color, (x, y, w, h), radius)

                    elif mode == "circle":
                        x1, y1 = start_pos
                        x2, y2 = end_pos

                        dx = x2 - x1
                        dy = y2 - y1
                        circle_radius = int((dx * dx + dy * dy) ** 0.5)

                        pygame.draw.circle(canvas, color, start_pos, circle_radius, radius)

                    drawing = False
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == "pen":
                        pygame.draw.circle(canvas, color, event.pos, radius)

                    elif mode == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, radius)

        screen.blit(canvas, (0, 0))

        info = "Mode: " + mode + " | Size: " + str(radius) + " | P pen, R rect, C circle, E eraser | 1 red 2 green 3 blue 4 white"
        font = pygame.font.SysFont("Verdana", 14)
        text = font.render(info, True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

main()