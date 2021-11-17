"""
Perlin terrain object.
30/10/21
"""
from perlin_noise import PerlinNoise
from math import sin

class PerlinTerrain:
    def __init__(this,  _nObjs=1,_freq=64,_amp=12,
                        _octs=3,_seed=99):
        this.noises = []
        this.seed = _seed
        this.seed = (ord('j')+ord('o'))
        this.freq = _freq
        this.amp = _amp
        this.octs = _octs

        for i in range(_nObjs):
            noise = PerlinNoise(octaves=this.octs,
                                seed=this.seed)
            this.noises.append(noise)
        
    def findHeight(this,_x,_z,sineBumps=True):
        from ursina import math
        y = 0
        for i in range(len(this.noises)):
            y += ((this.noises[i]([ _x/this.freq,
                                    _z/this.freq]))*
                                    this.amp/((i+1)))
        if sineBumps==True:
            y+= math.sin(_x)*1-0.5
            y+= math.cos(_z)*1-0.5
        return y