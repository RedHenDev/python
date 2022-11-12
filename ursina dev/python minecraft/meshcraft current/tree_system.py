print("Tree system module added.")
from random import randint
from perlin_module import PerlinNoise

class TreeSystem:
    @staticmethod
    def setup():

        TreeSystem.noisyEnt=PerlinNoise(seed=2020)
        TreeSystem.octaves = 1.0
        TreeSystem.freq = 320
        TreeSystem.amp = 18
        print("Tree system set up.")

    @staticmethod
    def growTree(x,z):
        # if randint(0,99) < 98:

        w=1+TreeSystem.noisyEnt(([x/TreeSystem.freq,
                                 z/TreeSystem.freq]))
        # w*=TreeSystem.amp                       
        print(w)
    
        if w>1.1:    
            # print("Ent not! ", w)
            return 0
        else:
            # 1 bark. 2 could be crown. Etc.
            # Would be cool to use an L-sytem, however.
            # print("Ent! ", w)
            return 0
            
            # print("Growing Ent!")

TreeSystem.setup()