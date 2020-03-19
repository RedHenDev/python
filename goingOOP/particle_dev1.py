"""
Developing a particle class.

19th March 2020
"""

import pygame as p
import random
from eulerClass import *

p.init()

# Window dimensions.
W = 800
H = 600

# Our pygame surface.
canvas = p.display.set_mode((W,H))

# Iterate over while loop to append new Euler particles to list.
lParticles = [Euler(canvas, p.Vector2(W/2,H/2), 12, "CIRCLE")]
lParticles[0].tCol = (0,200,0)
i = 0
total = 200
while i < total:
    newParticle = Euler(canvas,
                        p.Vector2(random.randint(0,W),random.randint(0,H)),
                        12, "CIRCLE")
    #newParticle.tCol = (255,255,255)
    lParticles.append(newParticle)
    i+=1

def checkInput():
    sMbutton = p.mouse.get_pressed()
    if sMbutton[0]:
        for pin in lParticles:
            # First, create vector pointing from mouse pos to particle pos.
            tempDir = pin.vPos - p.Vector2(p.mouse.get_pos()[0], p.mouse.get_pos()[1])
            # Next, add this (inversely) to the acceleration of the paticle.
            # Inversely, so that the nearer particles receive greater force.
            tempForce = 20
            pin.vAcc += tempDir * (1/tempDir.magnitude_squared()) * tempForce
        

# Update loop.
running = True
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    # Check mouse and key input.
    checkInput()

    # Repaint background of our pygame surface (canvas).
    canvas.fill((160,160,160))

    # Update our particles.
    index = -1
    for pp in lParticles:
        index += 1
        # First, add attraction force -- towards 0 indexed particle.
        # Not that we have exluded 0 particle from this process.
        if index > 0:
            #tempDir = lParticles[0].vPos - pp.vPos
            # Here we're asking the particles to be attracted towards current mouse pos.
            forceStrength = 9
            # tempDir = lSnakes[0].lSegments[0] - pp.vPos
            tempMP = p.mouse.get_pos()
            tempDir = p.Vector2(tempMP[0], tempMP[1]) - pp.vPos
            tempDist = 1/tempDir.magnitude_squared()
            # Make sure magnitude is above zero, else normalize function fails.
            #if tempDir.magnitude() <= 0: tempDir.scale_to_length(1)
            pp.vAcc += tempDir * tempDist * (forceStrength * 1)

            # Change colour according to velocity.
            # Crude mapping function.
            tempVal = pp.vVel.magnitude()/6 * 100
            tempVal = 255/100 * tempVal + 42
            if tempVal > 255: tempVal = 255
            
            pp.tCol = (tempVal, 0, tempVal)

        pp.limitSpeed(6)
        
        pp.update()
        # if index == 0: pp.overflow((W,H))
        pp.overflow((W,H))

        """
        # Collision with other particle?
        # If so, swap their velocities.
        for qq in lParticles:
            if qq == pp: continue
            elif Euler.checkCollision(pp, qq):
                Euler.swapVel(pp, qq)
                break
        """
                
        pp.render()

        # Black outline around each particle.
        """
        p.draw.circle(canvas, (0,0,0),
                      (int(pp.vPos.x),
                       int(pp.vPos.y)),
                      pp.iRad, 1)
        """
        
    # Render things to surface.
    p.display.flip()

p.quit()
