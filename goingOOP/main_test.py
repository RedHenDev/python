"""
Testing our first class.
Snake class.

4th March 2020

Comandeered (sp?) to dev particles and epidemic sim.
25th March-ish 2020
"""

import pygame as p
import random
from snakeClass import *
from eulerClass_epidemic import *

p.init()

# Epidemiology counter variables.
countStamp = 0
vulnerable = 0
infected = 0
immune = 0

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
total = 200
while i < total:
    newParticle = Euler(canvas,
                        p.Vector2(random.randint(0,W),random.randint(0,H)),
                        6, "CIRCLE")
    #newParticle.tCol = (255,255,255)
    if i < 60:
        newParticle.tCol = (0,200,0)
        immune += 1

    lParticles.append(newParticle)
    i+=1

# Patient zeroes!    
lParticles[99].tCol = (200,0,0)
lParticles[98].tCol = (200,0,0)
lParticles[97].tCol = (200,0,0)
lParticles[96].tCol = (200,0,0)
lParticles[95].tCol = (200,0,0)
infected = 5
vulnerable = total - infected - immune


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
            # Not any more. Now it's just towards current mouse pos.
            forceStrength = 1
            # tempDir = lSnakes[0].lSegments[0] - pp.vPos
            tempMP = p.mouse.get_pos()
            tempDir = p.Vector2(tempMP[0], tempMP[1]) - pp.vPos
            # Maybe this is better:
            # p.math.Vector2(p.mouse.get_pos()[0], p.mouse.get_pos()[1]))
            tempDist = tempDir.magnitude()
            if tempDir.magnitude() <= 0: tempDir.scale_to_length(1)
            pp.vAcc += tempDir.normalize() * 1/(tempDist * 1/forceStrength)

        pp.limitSpeed(7)
        
        pp.update()
        # if index == 0: pp.overflow((W,H))
        pp.overflow((W,H))
        
        # Collision with other particle?
        # If so, swap their velocities.
        # Note also counted infection increment here. Messy.
        for qq in lParticles:
            if qq == pp: continue
            elif Euler.checkCollision(pp, qq):
                infected += Euler.swapVel(pp, qq)
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
        
        #s.move()
        #s.overflow((W,H))
        #s.render()

    # Read out of infection change every ten seconds.
    if p.time.get_ticks() - countStamp > 10000:
        countStamp = p.time.get_ticks()
        vulnerable = total - immune - infected
        if vulnerable < 0: vulnerable = 0
        print("Infected = " + str(infected))
        print("Immune = " + str(immune))
        print("Vulnerable = " + str(vulnerable))
        print("Mouse xy = " + str(p.mouse.get_pos()))
        if vulnerable == 0:
            print("Simulation over. All that can be infected, have been.")
            running = False
        
    # Render things to surface.
    p.display.flip()

p.quit()
