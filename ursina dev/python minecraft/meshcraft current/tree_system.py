"""
Our Tree system :)
"""
from perlin_module import PerlinNoise
from ursina import Text

entText=Text('',scale=4)
class TreeSystem:
    @staticmethod
    def setup():
        # Create our Perlin noise object.
        treeOctaves=4
        treeSeed=2022
        TreeSystem.freq=16
        TreeSystem.amp=1
        TreeSystem.noise=PerlinNoise(
                octaves=treeOctaves,
                seed=treeSeed)

    def genTree(_x,_z):
        # Check whether to generate a tree here...

        ent=TreeSystem.noise(([  _x/TreeSystem.freq,
                                _z/TreeSystem.freq]))
        # entText.text='ent= ' + str(ent)
        # if ent>1.435:
        if ent*TreeSystem.amp>0.5: 
            return ent
        else:
            return 0


TreeSystem.setup()