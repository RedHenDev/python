"""
Testing our first class.
Snake class.

4th March 2020
"""

import pygame as p
import random
from snakeClass import *

p.init()

# Window dimensions.
W = 800
H = 600

# Our pygame surface.
canvas = p.display.set_mode((W,H))

lSnakes = [Snake(canvas, p.math.Vector2(W/2,H/2), 20, 3)]


def snakeExplosion(numberOfSneks, _vPosition):
    """Makes a number of random snakes explode from position passed in"""
    tempPos = p.math.Vector2(_vPosition.x, _vPosition.y)
    n = 0
    while n <  numberOfSneks:
        newSnake = Snake(canvas, tempPos,
                     random.randint(4,20), random.randint(3,7))
        lSnakes.append(newSnake)
        n += 1

def checkInput():
    sMbutton = p.mouse.get_pressed()
    if sMbutton[0]:
        snakeExplosion(10, p.math.Vector2(p.mouse.get_pos()))

# Begin with 10 sneks at centre of display.
snakeExplosion(10, p.math.Vector2(W/2, H/2))

# Have user control over these two sneks.
lSnakes[0].bAuto = False
lSnakes[9].bAuto = False


# Update loop.
running = True
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    # Check mouse and key input.
    checkInput()

    # Repaint background of our pygame surface (canvas).
    canvas.fill((120,0,120))

    # Update our snakes.
    for s in lSnakes:
        s.move()
        if random.randint(1,100) > 80 and s.bAuto: s.changeDirection()
        elif s.bAuto: s.directMe()
        s.overflow((W,H))
        s.render()
        
    # Render things to surface.
    p.display.flip()

p.quit()
