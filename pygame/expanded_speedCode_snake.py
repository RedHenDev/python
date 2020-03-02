"""
REFACTORED & DEVELOPED
March 1st 2020

Speedcoding Classic 'Snake' in Python :)

February 29th 2020

Red Hen

"""

import pygame as p
import random

p.init()

# font.init()

# Just grab user's default font.
# I.e. instead of failing to grab one they don't have.
font = p.font.Font(None, 20)

# Pi digits. Store as a string. In base 2.
pidB = "11.001001000011111101101010100010001000010110100011000010001101001100010011000110011000101000101110000000110111000001110011010001001010010000001"
pid = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"

timeStamp = 0

W = 850
H = 700

fillCol = (0,180,180)

bob = p.display.set_mode((W,H))

bob.fill(fillCol)

direction = 1

snake = [W/2,H/2]
step = 20


def appendSnake():
    snake.append(snake[len(snake)-2])
    snake.append(snake[len(snake)-2] + step)

noS = 1
i = 0
while i < noS:
    appendSnake()
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
    
    i = len(snake) - 1
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
    tCol2 = (242,242,242)

    # For counting number on body segment.
    # What could we do for pi day? Have the digits
    # of pi run along the body of the snake?
    number = 0
    
    i = 0
    while i < len(snake):
        tRec = (snake[i], snake[int(i+1)], step, step)
        tRec2 = (snake[i], snake[int(i+1)], step, step)
        if i < 2:
            blob = 4
            tCol2 = (0,0,0)
        else:
            blob = 2
            tCol2 = (200,200,200)
        p.draw.rect(bob, tCol, tRec)
        p.draw.rect(bob, tCol2, tRec2, blob)

        # Attempt at rendering text to display.
        origCol = (0, 51, 0)
        text = font.render(pid[number], True, tCol2)
        txtPos = (snake[i]+4, snake[int(i+1)]+4, step, step)
        bob.blit(text, txtPos)

        number += 1
        i += 2 

# What Digit of Pi variables.
wdop = 0
wX = 0
wY = 0

def spawnDigit():
    global snake, wdop, wX, wY

    wdop = pid[int(len(snake)/2)]
    wX = random.randint(12, W-12)
    wY = random.randint(12, H-12)

def renderDigit():
    # Attempt at rendering text to display.
    tCol = (200, 0, 0)
    text = font.render(wdop, True, tCol)
    txtPos = (wX, wY, 0, 0)
    bob.blit(text, txtPos)

def checkEat():
    global step, wY, wX, snake
    
    if (snake[0] - step) <= wX and (snake[0] + step) >= wX and \
    (snake[1] - step) <= wY and (snake[1] + step) >= wY:
        return True
    else: return False

spawnDigit()

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

    if checkEat():
        appendSnake()
        spawnDigit()
        
    
    renderDigit()

    renderSnake()
    
    p.display.flip()

p.quit()











