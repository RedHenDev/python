

print("Tree system module added.")
from random import randint

class TreeSystem:
    @staticmethod
    def growTree():
        if randint(0,99) < 98:
            # print("Ent not!")
            return 0
        else:
            # 1 bark. 2 could be crown. Etc.
            # Would be cool to use an L-sytem, however.
            return 1
            
            # print("Growing Ent!")