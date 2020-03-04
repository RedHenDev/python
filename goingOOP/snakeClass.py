"""Snake class
March 4th 2020
"""

import random # For randomizing self-directing snake movment.
import pygame # For use of 2D position vectors.

class Snake:
"""
Give positition (as (x,y) pygame.Vector2) and
length of snake as integer (includes head).
Give Step as float, which is size and movement
step of segments.
Finally, set Autonomous mode True or False,
for a self-directing snake.
"""
    def __init__(this, vPos, fStep, iLength=2,bAuto=True):
        this.vPos = vPos  # Am I copying the vector in the correct way here?
        this.fStep = fStep
        this.iLength = iLength
        this.bAuto = bAuto

        this.iDirection = random.randint(1,4)   # Up, Down, Left, and Right.
        this.lPositions  # The head segment occupies [0] in this list of 2D vectors.

        generateSnake()

    def generateSnake():

        # Position head according to position tuple passed in.
        this.IPositions[0] = this.tPos.x   # x.
        i = 1
        while i < this.iLength:
            appendSegment()

    def appendSegment():
        # Create temporary vector from last segment's position, minus step on y-axis.
        newPositionVector = pygame.math.Vector2(this.lPositions.x, this.lPositions.y - fStep)
        
        this.lSegments.append(newPositionVector) # Append new vector to list of segments.

    def renderSnake():

    def moveSnake():
        
