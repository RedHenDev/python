"""
Speedcoding Classic 'Snake' in Python :)

February 29th 2020

Red Hen

"""

import pygame as p

p.init()

timeStamp = 0

W = 850
H = 700

fillCol = (0,80,80)

bob = p.display.set_mode((W,H))

bob.fill(fillCol)

direction = 1

snake = [W/2,H/2]
step = 20

noS = 10
i = 0
while i < noS:
    snake.append(snake[len(snake)-2])
    snake.append(snake[len(snake)-1] + step)
    i += 1

def checkInput():
    global direction
    k = p.key.get_pressed()

    if k[p.K_UP]:
        direction = 1
    elif k[p.K_DOWN]:
        direction = 2
    elif k[p.K_LEFT]:
        direction = 3
    elif k[p.K_RIGHT]:
        direction = 4
        

def moveSnake():
    global direction
    i = len(snake) - 2
    while i > 1:
        snake[i] = snake[int(i-2)]
        i -= 1

    if direction == 1:
        snake[1] -= step
    elif direction == 2:
        snake[1] += step
    elif direction == 3:
        snake[0] -= step
    elif direction == 4:
        snake[0] += step
    

    



def renderSnake():

    tCol = (255,255,255)
    
    i = 0
    while i < len(snake) - 1:
        tRec = (snake[i], snake[int(i+1)], step, step)
        p.draw.rect(bob, tCol, tRec)
        i += 2 


running = True
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    bob.fill(fillCol)

    checkInput()
    
    timeNow = p.time.get_ticks()
    if timeNow - timeStamp > 500:
        moveSnake()
        timeStamp = p.time.get_ticks()

    renderSnake()
    
    p.display.flip()

p.quit()











