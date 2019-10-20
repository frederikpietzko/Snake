import random
import pygame
import sys

width = 500
rows = 20
delta = width // rows


grid = [[False for i in range(rows)] for j in range(rows)]

snake = [[5, 5, 0, 1], [5, 4, 0, 1], [5, 3, 0, 1]]
# direction can be (1,0) for right (-1,0) for left, (0, 1) for down and finally (0, -1) for up
direction = (0, 1)

food = (random.randint(0, 19), random.randint(0, 19), 0, 0)

window = pygame.display.set_mode((width, width))
clock = pygame.time.Clock()

def draw_grid():
    # important to do window.fill or display will overflow 
    window.fill((0, 0, 0))
    x, y = 0, 0
    for i in range(rows):
        x += delta
        y += delta
        pygame.draw.line(window, (255,255,255), (x, 0), (x, width))
        pygame.draw.line(window, (255,255,255), (0, y), (width, y))


def spawn_food():
    global food, snake
    x, y = random.randint(0, 19), random.randint(0, 19)
    while len(list(filter(lambda c: c[0] == x and c[1] == y, snake))) > 0:
        x, y = random.randint(0, 19), random.randint(0, 19)
    food = (x, y, 0, 0)


def draw_food():
    global food
    draw_cube(food, color=(0, 255, 0))


def eat_food():
    global snake, food
    x,y,_,_ = snake[0] 
    x2, y2, _, _ = food

    if x == x2 and y == y2:
        spawn_food()
        x, y, dx, dy = snake[-1]
        snake.append([x + (dx*-1), y + (dy*-1), dx, dy]) 

def draw_cube(pos, color=(255, 0, 0), eyes=False):
    global delta
    x, y,_,_ = pos
    pygame.draw.rect(window, color, (x * delta + 1, y * delta + 1, delta - 1, delta - 1))
    if eyes:
        centre = delta // 2
        radius = 3
        circle_middle = (x * delta + centre - radius, y * delta + 8)
        circle_middle_2 = (x * delta + centre - radius * 2, y * delta + 8)
        pygame.draw.circle(window, (0, 0, 0), circle_middle, radius)
        pygame.draw.circle(window, (0, 0, 0), circle_middle_2, radius)


def draw_snake():
    for i in range(len(snake)):
        cube = snake[i]
        draw_cube(cube, eyes=i==0)


def move_snake():
    global direction, rows, snake
    change_direction()
    set_cube_direction()
    for cube in snake:
        x, y, dx, dy = cube
        cube[0] += dx
        cube[1] += dy

        if cube[0] > rows - 1 and dx > 0:
            cube[0] = 0
        elif cube[0] < 0 and dx < 0:
            cube[0] = rows - 1
        elif cube[1] > rows - 1 and dy > 0:
            cube[1] = 0
        elif cube[1] < 0 and dy < 0:
            cube[1] = rows - 1
        
    if len(list(filter(lambda c: c[0] == snake[0][0] and c[1] == snake[0][1], snake[1:]))) > 0:
        sys.exit()

def change_direction():
    global direction, snake
    for event in pygame.event.get():
        x, y,_,_ = snake[0]

        if event.type == pygame.QUIT:
            pygame.quit()
        keys = pygame.key.get_pressed()
        cd = direction

        if keys[pygame.K_LEFT]:
            direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            direction = (1, 0)
        elif keys[pygame.K_UP]:
            direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            direction = (0, 1)
        
        if direction[0] * -1 == cd[0] and direction[1] * -1 == cd[1]:
            direction = cd


def set_cube_direction():
    global snake, direction
    dxh, dyh = None, None
    for i in range(len(snake)):
        x, y, dx, dy = snake[i]
        snake[i] = [x, y, dxh, dyh]
        dxh, dyh = dx, dy
    snake[0][2] = direction[0]
    snake[0][3] = direction[1]


while True:
    move_snake()
    eat_food()
    draw_grid()
    draw_snake()
    draw_food()
    pygame.time.delay(50)
    clock.tick(10)
    pygame.display.update()
