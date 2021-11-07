"""
Perlin terrain object.
30/10/21
"""
from perlin_noise import PerlinNoise
from math import sin

class PerlinTerrain:
    def __init__(this,  _nObjs=4,_freq=128,_amp=20,
                        _octs=8,_seed=99):
        this.noises = []
        this.seed = _seed
        this.seed = (ord('j')+ord('o'))
        this.freq = _freq
        this.amp = _amp
        this.octs = _octs

        for i in range(_nObjs):
            noise = PerlinNoise(octaves=this.octs-(i+1),
                                seed=this.seed)
            this.noises.append(noise)
        
    def findHeight(this,_x,_z,sineBumps=True):
        from ursina import math
        y = 0
        for i in range(len(this.noises)):
            y += ((this.noises[i]([ _x/this.freq*(0.1*i+1),
                                    _z/this.freq*(0.1*i+1)]))*
                                    this.amp/((i+1)*2))
        if sineBumps==True:
            y+= math.sin(_x)*1-0.5
            y+= math.cos(_z)*1-0.5
        return y