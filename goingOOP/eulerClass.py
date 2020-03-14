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
        this.sType = _sType

        this.tCol = (0,0,200 + random.randint(0,55))

        # Fields pertaining to Euler integration physics.
        # NB vPos above also part of this system.
        this.vVel = p.math.Vector2(0,0)
        this.vAcc = p.math.Vector2(0,0)

    def render(this):
        if this.sType == "CIRCLE":
            # First, we have to convert any vectors into tuples.
            tempPos = (int(this.vPos.x), int(this.vPos.y))
            p.draw.circle(this.surface, this.tCol, tempPos, this.iRad)
        elif this.sType == "SQUARE":
            # First, we have to convert any vectors into tuples, and
            # construct pygame Rectangle object.
            tempRect = (this.vPos.x, this.vPos.y, this.fRad, this.fRad)
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
            

            
