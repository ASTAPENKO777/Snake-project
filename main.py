import pygame
from random import randrange


RES = 800
SIZE = 50

x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
length = 1
snake = [(x, y)]
dx, dy = 0, 0
fps = 60
dirs = {'W': True, 'S': True, 'A': True, 'D': True}
score = 0
speed_count, snake_speed = 0, 10

high_score = 0

try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

pygame.init()
surface = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)
img = pygame.image.load('1.jpg').convert()

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def reset_game():
    global x, y, apple, length, snake, dx, dy, score, speed_count, snake_speed
    x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    score = 0
    speed_count = 0
    snake_speed = 10

while True:
    surface.blit(img, (0, 0))  
    close_game()  

    [pygame.draw.rect(surface, pygame.Color('green'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
    pygame.draw.rect(surface, pygame.Color('red'), (*apple, SIZE, SIZE))

    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    surface.blit(render_score, (5, 5))

    render_high_score = font_score.render(f'RECORD: {high_score}', 1, pygame.Color('yellow'))
    surface.blit(render_high_score, (5, 35))

    speed_count += 1
    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:] 

    if snake[-1] == apple:
        apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
        length += 1
        score += 1
        if snake_speed > 4: 
            snake_speed -= 1

    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))

        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            surface.blit(render_end, (RES // 2 - 200, RES // 3))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    break
            else:
                continue
            break

    pygame.display.flip()
    clock.tick(fps)

    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_s] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True}
