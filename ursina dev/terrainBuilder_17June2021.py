""" Perlin noise experiments """
""" 
Build terrain for Minecraft Python.
15th June 2021
Opened on PC at CCC 17th June 2021
"""

from ursina import *
from ursina.mesh_importer import *
import numpy as nn
import random as ra
import math

#from pnoise import pnoise2
from perlin_noise import PerlinNoise

def input(key):
    global currentZ,currentX
    if key == 'q' or key == 'escape': 
        exit()

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

# Perlin noise setup.
noise = PerlinNoise(octaves=3,seed=1988)

# Our terrain object.
urizen = Entity()
urizen.model=None
urizen.collider = None
# Our block object.
bub = Entity(model='cube',collider=None,parent=urizen)
# Terrain data.
urizenData = []
terrainWidth = 30
for i in range (terrainWidth*terrainWidth): 
    bub.x = x = math.floor(i/terrainWidth)
    bub.z = z = math.floor(i%terrainWidth)
    freq = 64
    amp = 24
    y = (noise([x/freq,z/freq])* amp)
    bub.y = y = math.floor(y)
    urizenData.append(y)
    urizen.combine(auto_destroy=False)

destroy(bub)
urizen.texture = 'grass_14.png'
urizen.collider='mesh'    



# Can we save the terrain?
#Mesh.save(urizen.model, 'bobby.obj')
EditorCamera()
app.run()
