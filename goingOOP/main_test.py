"""
Testing our first class.
Snake class.

4th March 2020
"""

import pygame as p
import random
from snakeClass import *
from eulerClass import *

p.init()

# Window dimensions.
W = 800
H = 600

# Our pygame surface.
canvas = p.display.set_mode((W,H))

lSnakes = [Snake(canvas, p.math.Vector2(W/2,H/2), 20, 7)]

# Iterate over while loop to append new Euler particles to list.
lParticles = [Euler(canvas, p.Vector2(W/2,H/2), 12, "CIRCLE")]
lParticles[0].tCol = (0,200,0)
i = 0
while i < 111:
    newParticle = Euler(canvas,
                        p.Vector2(random.randint(0,W),random.randint(0,H)),
                        6, "CIRCLE")
    #newParticle.tCol = (255,255,255)
    lParticles.append(newParticle)
    i+=1

# Patient zero!    
lParticles[12].tCol = (200,0,0)

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
    if sMbutton[1]:
        snakeExplosion(10,
                       p.math.Vector2(p.mouse.get_pos()[0], p.mouse.get_pos()[1]))
    if sMbutton[0]:
        for pp in lParticles:
            pp.vAcc.y += random.uniform(-0.1, 0.1)
            pp.vAcc.x += random.uniform(-0.1, 0.1)
        

# Begin with 100 sneks at centre of display.
#snakeExplosion(100, p.math.Vector2(W/2, H/2))

# Have user control over these two sneks.
lSnakes[0].bAuto = False
#lSnakes[9].bAuto = False


# Update loop.
running = True
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    # Check mouse and key input.
    checkInput()

    # Repaint background of our pygame surface (canvas).
    canvas.fill((200,200,200))

    # Update our particles.
    index = -1
    for pp in lParticles:
        index += 1
        # First, add attraction force -- towards 0 indexed particle.
        if index > 0:
            #tempDir = lParticles[0].vPos - pp.vPos
            # Here we're asking the particles to be attracted to the head
            # of the first snake on the list, the user-controlled serpent.
            forceStrength = 1
            tempDir = lSnakes[0].lSegments[0] - pp.vPos
            tempDist = tempDir.magnitude()
            pp.vAcc += tempDir.normalize() * 1/(tempDist * 1/forceStrength)

        pp.limitSpeed(7)
        
        pp.update()
        if index == 0: pp.overflow((W,H))
        
        # Collision with other particle?
        # If so, swap their velocities.
        for qq in lParticles:
            if qq == pp: continue
            elif Euler.checkCollision(pp, qq):
                Euler.swapVel(pp, qq)
                break
        
                
        pp.render()
        
        p.draw.circle(canvas, (0,0,0),
                      (int(pp.vPos.x),
                       int(pp.vPos.y)),
                      pp.iRad, 1)

    # Update our snakes.
    for s in lSnakes:
        if random.randint(1,100) > 98 and s.bAuto: s.changeDirection()
        elif s.bAuto==False: s.directMe()
        
        s.move()
        s.overflow((W,H))
        s.render()

    
        
    # Render things to surface.
    p.display.flip()

p.quit()
