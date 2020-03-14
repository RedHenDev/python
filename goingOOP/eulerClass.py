"""Class of 'euler' particles"""

""" 14th March 2020 """

import pygame as p # For vector object and rendering shapes.
import random

class Euler:
    """surface vPos fRadius sType"""
    def __init__(this, _pygameSurface, _vPos, _fRad, _sType):

        # Pygame surface reference, so that we can render somewhere.
        this.surface = _pygameSurface
        
        this.vPos = p.math.Vector2(_vPos.x, _vPos.y)
        this.iRad = int(_fRad)
        this.halfRad = this.iRad * 0.5  # Calculate half radius now: efficiency.
        this.sType = _sType

        this.tCol = (0,0,200 + random.randint(0,55))

        # Fields pertaining to Euler integration physics.
        # NB vPos above also part of this system.
        this.vVel = p.math.Vector2(0,0)
        this.vAcc = p.math.Vector2(0,0)

    # Static functions?
    # Ah, we must use a decorator, whatever that means, and which
    # takes no self-object argument.
    @staticmethod
    def checkCollision(_ob1, _ob2):
        """Check whether objects are overlapping"""
        if _ob1.vPos.distance_to(_ob2.vPos) < _ob1.iRad + _ob2.iRad:
           return True
        else: return False

    @staticmethod
    def swapVel(_ob1, _ob2):
        """Swap velocities of these two objects"""
        tempVel = p.Vector2(_ob1.vVel.x, _ob1.vVel.y)
        _ob1.vVel = _ob2.vVel
        _ob2.vVel = tempVel

    def render(this):
        if this.sType == "CIRCLE":
            # First, we have to convert any vectors into tuples.
            # Position is offset by half radius, so that position is centred.
            tempPos = (int(this.vPos.x - this.halfRad), int(this.vPos.y - this.halfRad))
            p.draw.circle(this.surface, this.tCol, tempPos, this.iRad)
        elif this.sType == "SQUARE":
            # First, we have to convert any vectors into tuples, and
            # construct pygame Rectangle object.
            # Position is offset by half radius, so that position is centred.
            tempRect = (this.vPos.x - this.halfRad, this.vPos.y - this.halfRad, this.fRad, this.fRad)
            p.draw.rect(this.surface, this.tCol, tempRect)

    def update(this):
        """Euler physics"""
        this.vVel += this.vAcc
        this.vPos += this.vVel

        this.vAcc.xy = 0,0

    def overflow(this, _tWH):
        """Pac-man overflow from one side of screen to other"""
        """NB. width & height passed as a tuple"""
        if this.vPos.x < 0:
            this.vPos.x = _tWH[0]
        elif this.vPos.x > _tWH[0]:
            this.vPos.x = 0

        if this.vPos.y < 0:
            this.vPos.y = _tWH[1]
        elif this.vPos.y > _tWH[1]:
            this.vPos.y = 0

    

            
