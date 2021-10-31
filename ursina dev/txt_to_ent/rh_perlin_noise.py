"""
Perlin terrain object.
30/10/21
"""
from perlin_noise import PerlinNoise
from math import sin

class PerlinTerrain:
    def __init__(this,  _nObjs=3,_freq=512,_amp=16,
                        _octs=8,_seed=99):
        this.noises = []
        this.seed = _seed
        this.seed = (ord('j')+ord('o'))
        this.freq = _freq
        this.amp = _amp
        this.octs = _octs

        for i in range(_nObjs):
            noise = PerlinNoise(octaves=this.octs-i,
                                seed=this.seed)
            this.noises.append(noise)
        
    def findHeight(this,_x,_z,sineBumps=True):
        y = 0
        for i in range(len(this.noises)):
            y += ((this.noises[i]([ _x/this.freq,
                                    _z/this.freq]))*
                                    this.amp/(i+1))
        if sineBumps==True:
            y+= sin(_x)*0.5-0.5
        return y