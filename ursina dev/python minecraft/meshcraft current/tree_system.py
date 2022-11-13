print("Tree system module added.")
from random import randint
from perlin_module import PerlinNoise

class TreeSystem:
    @staticmethod
    def setup():

        Toctaves = 32
        TreeSystem.noisyEnt=PerlinNoise(octaves=Toctaves,
                                        seed=2020)
        
        TreeSystem.freq = 64
        # TreeSystem.amp = 100
        print("Tree system set up.")

    @staticmethod
    def growTree(x,z):
        # if randint(0,99) < 98:

        w=1+TreeSystem.noisyEnt(([x/TreeSystem.freq,
                                 z/TreeSystem.freq]))
        # w*=TreeSystem.amp                       
        # print(w)
        # 1.42
        if w>1.435:    
            # print("Ent not! ", w)
            return w
        else:
            # 1 bark. 2 could be crown. Etc.
            # Would be cool to use an L-sytem, however.
            # print("Ent! ", w)
            return 0
            
            # print("Growing Ent!")

TreeSystem.setup()