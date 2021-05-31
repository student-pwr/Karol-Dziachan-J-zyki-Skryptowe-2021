import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from random import randint
import pl.karol.dziachan.snake.statics as statics

width = 500
height = 500
win = pygame.display.set_mode((width, height))

pygame.display.set_caption('Pygame')

# Colors

red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)
black = (0, 0, 0)



class Part(object):
    rows = 20

    def __init__(self, start, direction_x=1, direction_y=0, color=((41, 55, 65))):
        self.tmp_pos = start
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.color = color

    #to move one part of snake
    def go_snake(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.tmp_pos = (self.tmp_pos[0] + self.direction_x, self.tmp_pos[1] + self.direction_y)

    #draw parts of snake on the screen
    def draw(self, area, eyes=False):
        dis = size // rows
        rw = self.tmp_pos[0]
        cm = self.tmp_pos[1]
        pygame.draw.rect(area, self.color, (rw * dis + 1, cm * dis + 1, dis - 2, dis - 2))
        
        #draw eye of snake to better look
        if eyes:
            center = dis // 2
            rad = 3
            eye_0 = (rw * dis + center - rad - 2, cm * dis + 8)
            eye_1 = (rw * dis + dis - rad * 2, cm * dis + 8)
            pygame.draw.circle(area, (255, 255, 255), eye_0, rad)
            pygame.draw.circle(area, (255, 255, 255), eye_1, rad)


class Snake(object):
    snake_body = []
    snake_turns = {}

    def __init__(self, color, tmp_pos):
        self.snake_body = []
        self.color = color
        self.head = Part(tmp_pos)
        self.snake_body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1
        self.score = 0

    def go_snake(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.direction_x = -1
                self.direction_y = 0
                self.snake_turns[self.head.tmp_pos[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_RIGHT]:
                self.direction_x = 1
                self.direction_y = 0
                self.snake_turns[self.head.tmp_pos[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_UP]:
                self.direction_x = 0
                self.direction_y = -1
                self.snake_turns[self.head.tmp_pos[:]] = [self.direction_x, self.direction_y]
            elif keys[pygame.K_DOWN]:
                self.direction_x = 0
                self.direction_y = 1
                self.snake_turns[self.head.tmp_pos[:]] = [self.direction_x, self.direction_y]

        for i, par in enumerate(self.snake_body):
            p = par.tmp_pos[:]
            if p in self.snake_turns:
                turn = self.snake_turns[p]
                par.go_snake(turn[0], turn[1])
                if i == len(self.snake_body) - 1:
                    self.snake_turns.pop(p)
            else:
                if par.direction_x == -1 and par.tmp_pos[0] <= 0:
                    par.tmp_pos = (par.rows - 1, par.tmp_pos[1])
                elif par.direction_x == 1 and par.tmp_pos[0] >= par.rows - 1:
                    par.tmp_pos = (0, par.tmp_pos[1])
                elif par.direction_y == 1 and par.tmp_pos[1] >= par.rows - 1:
                    par.tmp_pos = (par.tmp_pos[0], 0)
                elif par.direction_y == -1 and par.tmp_pos[1] <= 0:
                    par.tmp_pos = (par.tmp_pos[0], par.rows - 1)
                else:
                    par.go_snake(par.direction_x, par.direction_y)

    def new_game(self, tmp_pos):
        self.head = Part(tmp_pos)
        self.snake_body = []
        self.snake_body.append(self.head)
        self.snake_turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def add_to_body(self):
        tail = self.snake_body[-1]
        dir_x, dir_y = tail.direction_x, tail.direction_y

        self.score += 1

        if dir_x == 1 and dir_y == 0:
            self.snake_body.append(Part((tail.tmp_pos[0] - 1, tail.tmp_pos[1])))
        elif dir_x == -1 and dir_y == 0:
            self.snake_body.append(Part((tail.tmp_pos[0] + 1, tail.tmp_pos[1])))
        elif dir_x == 0 and dir_y == 1:
            self.snake_body.append(Part((tail.tmp_pos[0], tail.tmp_pos[1] - 1)))
        elif dir_x == 0 and dir_y == -1:
            self.snake_body.append(Part((tail.tmp_pos[0], tail.tmp_pos[1] + 1)))

        self.snake_body[-1].direction_x = dir_x
        self.snake_body[-1].direction_y = dir_y

    def draw(self, area):
        for i, par in enumerate(self.snake_body):
            if i == 0:
                par.draw(area, True)
            else:
                par.draw(area)


def play_game():
    global size, rows, s, apple
    size = 500
    rows = 20

    window = pygame.display.set_mode((size, size))

    s = None
    s = Snake((41, 55, 65), (10, 10))
    apple = Part(statics.draw_apple(s, rows), color=(200, 0, 0))

    mode = True
    clock = pygame.time.Clock()
    quit = True

    while mode:

        pygame.time.delay(50)
        clock.tick(10)
        s.go_snake()
        if s.snake_body[0].tmp_pos == apple.tmp_pos:
            s.add_to_body()
            apple = Part(statics.draw_apple(s, rows), color=(240, 0, 0))

        for x in range(len(s.snake_body)):
            if s.snake_body[x].tmp_pos in list(map(lambda z: z.tmp_pos, s.snake_body[x + 1:])):
                quit = False
                with open("score_ss.txt", "r") as f:
                    if int(f.read(1)) < s.score:
                        f.close()
                        with open("score_ss.txt", "w") as g:
                            g.write(str(s.score))
                pygame.quit()
                menu()
            break

        if quit:
            statics.draw_window(window, s, apple, size, rows)
        else:
            break

def menu():
    menu = True
    quit = True
    while menu:
        pygame.init()
        win = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake')
        win.fill(black)

        font = pygame.font.SysFont('Time New Roman', 60)

        title = font.render('SNAKE', False, green)
        titleRect = title.get_rect()
        titleRect.center = (width // 2, 100)
        win.blit(title, titleRect)

        with open("score_ss.txt", "r") as h:
            tmp_high_score = int(h.read(1))

        high = font.render('High Score: ' + str(tmp_high_score), False, purple)
        highRect = high.get_rect()
        highRect.center = (width // 2, height // 2)
        win.blit(high, highRect)

        quit = font.render('Press Q to Quit', False, ((randint(0, 255), randint(0, 255), randint(0, 255))))
        quitRect = quit.get_rect()
        quitRect.center = (width // 2, height // 2 + 100)
        win.blit(quit, quitRect)

        start = font.render('Press Space to Start', False, ((randint(0, 255), randint(0, 255), randint(0, 255))))
        startRect = start.get_rect()
        startRect.center = (width // 2, height - 50)
        win.blit(start, startRect)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            play_game()
        elif key[pygame.K_q]:
            quit = False
            pygame.quit()


        if quit:
            pygame.display.update()

class Play:
    menu()
