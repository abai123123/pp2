import pygame
import math
from datetime import datetime
from collections import deque

def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        px, py = q.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)

        q.append((px + 1, py))
        q.append((px - 1, py))
        q.append((px, py + 1))
        q.append((px, py - 1))


def main():
    pygame.init()

    WIDTH = 1000
    HEIGHT = 650

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))

    font = pygame.font.SysFont("Verdana", 14)
    text_font = pygame.font.SysFont("Verdana", 28)

    mode = "pencil"
    color = (0, 0, 255)
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None

    text_mode = False
    text_pos = None
    current_text = ""

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        preview = canvas.copy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return

                if event.key == pygame.K_s and ctrl_held:
                    filename = "paint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                    pygame.image.save(canvas, filename)

                elif text_mode:
                    if event.key == pygame.K_RETURN:
                        rendered = text_font.render(current_text, True, color)
                        canvas.blit(rendered, text_pos)
                        text_mode = False
                        current_text = ""
                        text_pos = None

                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        current_text = ""
                        text_pos = None

                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]

                    else:
                        current_text += event.unicode

                else:
                    if event.key == pygame.K_ESCAPE:
                        return

                    if event.key == pygame.K_p:
                        mode = "pencil"
                    elif event.key == pygame.K_l:
                        mode = "line"
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
                    elif event.key == pygame.K_f:
                        mode = "fill"
                    elif event.key == pygame.K_x:
                        mode = "text"

                    elif event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

                    elif event.key == pygame.K_q:
                        color = (255, 0, 0)
                    elif event.key == pygame.K_w:
                        color = (0, 255, 0)
                    elif event.key == pygame.K_a:
                        color = (0, 0, 255)
                    elif event.key == pygame.K_d:
                        color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mode == "fill":
                        flood_fill(canvas, event.pos[0], event.pos[1], color)

                    elif mode == "text":
                        text_mode = True
                        text_pos = event.pos
                        current_text = ""

                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

                        if mode == "pencil":
                            pygame.draw.circle(canvas, color, event.pos, brush_size)

                        elif mode == "eraser":
                            pygame.draw.circle(canvas, (0, 0, 0), event.pos, brush_size)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing and start_pos is not None:
                    end_pos = event.pos
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    if mode == "line":
                        pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

                    elif mode == "rectangle":
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

                    elif mode == "square":
                        size = min(abs(x2 - x1), abs(y2 - y1))
                        x = x1 - size if x2 < x1 else x1
                        y = y1 - size if y2 < y1 else y1
                        pygame.draw.rect(canvas, color, (x, y, size, size), brush_size)

                    elif mode == "circle":
                        dx = x2 - x1
                        dy = y2 - y1
                        r = int((dx * dx + dy * dy) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, brush_size)

                    elif mode == "right_triangle":
                        points = [(x1, y1), (x2, y1), (x1, y2)]
                        pygame.draw.polygon(canvas, color, points, brush_size)

                    elif mode == "equilateral_triangle":
                        side = abs(x2 - x1)
                        h = int(side * math.sqrt(3) / 2)

                        if x2 >= x1:
                            points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - h)]
                        else:
                            points = [(x1, y1), (x1 - side, y1), (x1 - side // 2, y1 - h)]

                        pygame.draw.polygon(canvas, color, points, brush_size)

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

                        pygame.draw.polygon(canvas, color, points, brush_size)

                    drawing = False
                    start_pos = None
                    last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == "pencil":
                        pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                        last_pos = event.pos

                    elif mode == "eraser":
                        pygame.draw.line(canvas, (0, 0, 0), last_pos, event.pos, brush_size)
                        last_pos = event.pos

        if drawing and start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            x1, y1 = start_pos
            x2, y2 = mouse_pos

            if mode == "line":
                pygame.draw.line(preview, color, start_pos, mouse_pos, brush_size)

            elif mode == "rectangle":
                x = min(x1, x2)
                y = min(y1, y2)
                w = abs(x2 - x1)
                h = abs(y2 - y1)
                pygame.draw.rect(preview, color, (x, y, w, h), brush_size)

            elif mode == "square":
                size = min(abs(x2 - x1), abs(y2 - y1))
                x = x1 - size if x2 < x1 else x1
                y = y1 - size if y2 < y1 else y1
                pygame.draw.rect(preview, color, (x, y, size, size), brush_size)

            elif mode == "circle":
                dx = x2 - x1
                dy = y2 - y1
                r = int((dx * dx + dy * dy) ** 0.5)
                pygame.draw.circle(preview, color, start_pos, r, brush_size)

        screen.blit(preview, (0, 0))

        if text_mode and text_pos is not None:
            rendered = text_font.render(current_text + "|", True, color)
            screen.blit(rendered, text_pos)

        info1 = "Mode: " + mode + " | Brush: " + str(brush_size)
        info2 = "P pencil | L line | R rect | S square | C circle | T right tri | U equi tri | H rhombus | F fill | E eraser | X text"
        info3 = "Brush size: 1 small | 2 medium | 3 large | Colors: Q red | W green | A blue | D white | Ctrl+S save"

        text1 = font.render(info1, True, (255, 255, 255))
        text2 = font.render(info2, True, (255, 255, 255))
        text3 = font.render(info3, True, (255, 255, 255))

        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))
        screen.blit(text3, (10, 50))

        pygame.display.flip()
        clock.tick(60)

main()