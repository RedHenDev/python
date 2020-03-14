"""Snake class
March 4th 2020
"""

import random # For randomizing self-directing snake movement.
import pygame # For use of 2D position vectors and rendering snake.
import pygame.math # Needed by pygame for vectors. Apparently. Doubt it.

"""
First, specify the pygame surface snake to be
rendered to. Used with pygame.draw.rect().
Give positition (as (x,y) pygame.Vector2) and
length of snake as integer (includes head).
Give Step as float, which is size and movement
step of segments.
Finally, set Autonomous mode True or False,
for a self-directing snake.
"""
class Snake:
    """Snake(pygame.surface, position, step, length, autonomous=True)"""
    def __init__(this, surface ,vPos, fStep, iLength=2,bAuto=True):
        this.surface = surface
        # Am I copying the vector in the correct way here?
        this.vPos = pygame.math.Vector2(vPos.x, vPos.y)
        this.fStep = fStep
        this.iLength = iLength
        this.bAuto = bAuto

        # Which segment to display as green.
        # Start at index 1, so as to miss out head (for aesthetics).
        this.iGreenID = 1

        # Time fields, for controlling speed of snake movement.
        this.fTimeStamp = pygame.time.get_ticks()
        this.fSpeed = random.randint(12, 512)
        
        # Up, Down, Left, and Right.
        this.iDirection = random.randint(0,3)
        # List of useful pygame vectors for UP, DOWN, LEFT, AND RIGHT.
        this.lDirections = [
                            pygame.Vector2(0,-1),
                            pygame.Vector2(0,1),
                            pygame.Vector2(-1,0),
                            pygame.Vector2(1,0)
                            ]

        # The head segment occupies [0] in this list of 2D vectors.
        # Position head according to position vector passed in.
        this.lSegments = [this.vPos]

        def appendSegment(this):
            # Create temporary vector from last segment's position, minus step on y-axis.
            newPositionVector = pygame.math.Vector2(this.lSegments[-1].x, this.lSegments[-1].y - this.fStep)
            this.lSegments.append(newPositionVector) # Append new vector to list of segments.

        def generateSnake(this):

            i = 1
            while i < this.iLength:
                appendSegment(this)
                i += 1

        generateSnake(this)

    def render(this):
        # Iterate over segments and draw a square. Adjust so that each position is at centre
        # of its square, rather than the default top left corner.
        i = 0
        while i < len(this.lSegments):
            if this.iGreenID >= i and this.iGreenID < i+1:
                tempCol = (0,220,0)
            else: tempCol = (255,255,255)
            tempRect = (this.lSegments[i].x - this.fStep * 0.5,
                        this.lSegments[i].y - this.fStep * 0.5, this.fStep, this.fStep)
            pygame.draw.rect(this.surface, tempCol, tempRect)

            # Black outline.
            pygame.draw.rect(this.surface, (0,0,0), tempRect, 2)
            i += 1

        

    def overflow(this, _tWH):
        """Overflow segment from one side of display to other. tWH tuple Width&Height"""
        i = 0
        while i < len(this.lSegments):
            tempSeg = this.lSegments[i]
            if tempSeg.x < 0 - this.fStep:
                this.lSegments[i].x = _tWH[0]
            if tempSeg.x > _tWH[0] + this.fStep:
                this.lSegments[i].x = 0
            if tempSeg.y < 0 - this.fStep:
                this.lSegments[i].y = _tWH[1]
            if tempSeg.y > _tWH[1] + this.fStep:
                this.lSegments[i].y = 0
            i += 1

    def move(this, _timed=True):
        """Move head in iDirection (0-3), then iterate over other segments, reverse order."""

        # First, check whether time to move (if snek is timed).
        timeNow = pygame.time.get_ticks()
        if _timed and timeNow - this.fTimeStamp >= this.fSpeed:
            this.fTimeStamp = pygame.time.get_ticks()
        elif _timed: return
        
        i = len(this.lSegments) -1
        # Greater than 0 since we move the head independently.
        while i > 0:
            this.lSegments[i].x = this.lSegments[int(i-1)].x
            this.lSegments[i].y = this.lSegments[int(i-1)].y
            i -= 1

        this.lSegments[0].x += this.lDirections[this.iDirection].x * this.fStep
        this.lSegments[0].y += this.lDirections[this.iDirection].y * this.fStep

        # Advance green segment.
        this.iGreenID += 1
        if this.iGreenID > len(this.lSegments):
            this.iGreenID = 1

    def changeDirection(this):
        """Randomly pick new iDirection (0-3)."""
        this.iDirection = random.randint(0,3)

    def directMe(this):
        """Use WSAD or Arrows to control snake direction"""
        """Pygame key.get_pressed() used to collect input (a list)"""
        whichKeys = pygame.key.get_pressed()
        if whichKeys[pygame.K_w] or whichKeys[pygame.K_UP]:
            this.iDirection = 0
        elif whichKeys[pygame.K_s] or whichKeys[pygame.K_DOWN]:
            this.iDirection = 1
        elif whichKeys[pygame.K_a] or whichKeys[pygame.K_LEFT]:
            this.iDirection = 2
        elif whichKeys[pygame.K_d] or whichKeys[pygame.K_RIGHT]:
            this.iDirection = 3






            
