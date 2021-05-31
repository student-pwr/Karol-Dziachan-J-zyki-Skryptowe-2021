import random
from tkinter import messagebox

import pygame
from random import randint



def draw_grid(w, rows, area):
    size_between = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(area, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(area, (255, 255, 255), (0, y), (w, y))


def draw_window(area, s, apple, size, rows):
    area.fill((0, 180, 0))
    s.draw(area)
    apple.draw(area)
    draw_grid(size, rows, area)
    pygame.display.update()





def draw_apple(snake, rows):
    tmp_positions = snake.snake_body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.tmp_pos == (x,y), tmp_positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content, tk):
    root = tk.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass
