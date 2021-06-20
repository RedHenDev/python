"""Terrain 0.1"""

from ursina import *

app = Ursina()

def input(key):
    if key == 'q' or key == 'escape':
        exit()
    


e = Entity(model=Terrain('grass_12', skip=9), scale=(20,5,20), texture='grass_12')

EditorCamera()

app.run()
