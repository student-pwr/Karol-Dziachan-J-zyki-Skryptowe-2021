import pygame
from random import randint

pygame.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))

pygame.display.set_caption('Cleaner')



red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)
black = (0, 0, 0)



class Cleaner(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25, 25])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.score = 0
        with open("score_snake.txt", "r") as h:
            self.highScore = int(h.read(1))


        self.speed = 10
        self.direct_x = 0
        self.direct_y = 0


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()

    def move(self):
        food.rect.x = randint(50, width - 50)
        food.rect.y = randint(50, height - 50)


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25, 25])
        self.image.fill(purple)
        self.rect = self.image.get_rect()



cleaner = Cleaner()
cleaner.rect.x = width // 2
cleaner.rect.y = height // 2

food = Food()
food.rect.x = randint(50, width - 50)
food.rect.y = randint(50, height - 50)


sprites_group = pygame.sprite.Group()
sprites_group.add(cleaner)
sprites_group.add(food)

bomb_group = pygame.sprite.Group()


def redraw():
    if playing:
        win.fill(green)


        font = pygame.font.SysFont('Time New Roman', 24)
        score = font.render('SCORE: ' + str(cleaner.score), False, black)
        scoreRect = score.get_rect()
        scoreRect.center = (width // 2, 50)
        win.blit(score, scoreRect)


        sprites_group.update()
        sprites_group.draw(win)
        bomb_group.update()
        bomb_group.draw(win)
    else:
        win.fill(black)

        font = pygame.font.SysFont('Time New Roman', 60)


        title = font.render('CLEANER', False, green)
        titleRect = title.get_rect()
        titleRect.center = (width // 2, 100)
        win.blit(title, titleRect)


        high = font.render('High Score: ' + str(cleaner.highScore), False, purple)
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

    pygame.display.update()


running = True
playing = False

while running:

    pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if playing:
        cleaner.rect.x += cleaner.direct_x
        cleaner.rect.y += cleaner.direct_y


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            cleaner.direct_x = -cleaner.speed
            cleaner.direct_y = 0
        if key[pygame.K_RIGHT]:
            cleaner.direct_x = cleaner.speed
            cleaner.direct_y = 0
        if key[pygame.K_UP]:
            cleaner.direct_x = 0
            cleaner.direct_y = -cleaner.speed
        if key[pygame.K_DOWN]:
            cleaner.direct_x = 0
            cleaner.direct_y = cleaner.speed

        if cleaner.rect.colliderect(food.rect):
            food.move()
            bomb = Bomb()
            bomb.rect.x = cleaner.rect.x + 50
            bomb.rect.y = cleaner.rect.y + 50
            bomb_group.add(bomb)
            cleaner.score += 1

        for bomb in bomb_group:
            if bomb.rect.colliderect(cleaner.rect):
                if cleaner.score > cleaner.highScore:
                    cleaner.highScore = cleaner.score
                playing = False

    else:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            playing = True
            cleaner.rect.x = width // 2
            cleaner.rect.y = height // 2
            cleaner.score = 0
            bomb_group.empty()
        elif key[pygame.K_q]:
            with open("score_snake.txt", "r") as f:
                if int(f.read(1)) < cleaner.highScore:
                    f.close()
                    with open("score_snake.txt", "w") as g:
                        g.write(str(cleaner.highScore))
            pygame.quit()
            break
    redraw()

pygame.quit()