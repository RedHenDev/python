"""
Our Tree system :)
"""
from perlin_module import PerlinNoise
from ursina import Text, random
from math import sin,cos

entText=Text('',scale=4)
class TreeSystem:
    @staticmethod
    def setup():
        # Create our Perlin noise object.
        treeOctaves=8
        treeSeed=random.randint(1,10000)
        TreeSystem.freq=256
        TreeSystem.amp=10
        TreeSystem.noise=PerlinNoise(
                octaves=treeOctaves,
                seed=treeSeed)

    def genTree(_x,_z):
        # Check whether to generate a tree here...
        if _x % 2==0: return 0
        if _z % 2==0:return 0
        if _x % 3==0: return 0
        if _z % 3==0:return 0
        if _x % 5==0: return 0
        if _z % 5==0:return 0

        ent=TreeSystem.noise(([  _x/TreeSystem.freq,
                                _z/TreeSystem.freq]))
        ent*=TreeSystem.amp
        # entText.text='ent= ' + str(ent)
        # if ent>1.435:
        if ent>1: 
            return ent
        else:
            return 0


TreeSystem.setup()