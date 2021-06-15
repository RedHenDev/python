""" Perlin noise experiments """
""" 
Build terrain for Minecraft Python.
15th June 2021
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

class Block:
    def __init__(this, _scale):
        this.ent = Entity(model="cube",color=color.white,
                          scale=_scale,texture='grass_mono.png')
        this.origColor = this.ent.color

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=1988)

# Our terrain object.
urizen = Entity()

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 100
for i in range(blocksWidth*blocksWidth):
    bub = Block(1)
    bub.ent.scale_y = 1
    bub.ent.x = math.floor(i/blocksWidth)
    bub.ent.z = math.floor(i%blocksWidth)
    bub.ent.parent = urizen
    blocks.append(bub)

# Terrain data.
urizenData = []
terrainWidth = 100
for i in range (terrainWidth*terrainWidth): 
    x = math.floor(i/terrainWidth)
    z = math.floor(i%terrainWidth)
    freq = 64
    amp = 12
    y = (noise([x/freq,z/freq])* amp)
    y = math.floor(y)
    urizenData.append(y)

def generateChunk(_ox, _oz):
    global terrainWidth, blocksWidth, realPosX, realPosZ
    global currentZ, currentX
    urizen.model=None
    for i in range(blocksWidth*blocksWidth):
        x = realPosX + math.floor(_ox + math.floor(i/blocksWidth))
        z = realPosZ + math.floor(_oz + math.floor(i%blocksWidth))
        # Check index. If out of range, return to default
        # chunk position.
        indi = int((x*terrainWidth)+z)
        
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                y = blocks[i].ent.y = 0
        else: y = blocks[i].ent.y = urizenData[indi]

        # Decide colour of each block according to height.
        r = 160 + y * 10
        g = 160 + y * 42
        b = 0
        blocks[i].ent.color=color.rgb(r,g,b)
    
    for b in blocks:
        b.ent.enable()
    urizen.combine(auto_destroy=False)
    for b in blocks:
        b.ent.disable()
    urizen.collider = 'mesh'
    urizen.texture = 'grass_mono.png'
    # Centre subject relative to chunk.
    urizen.x = math.floor(-blocksWidth*0.5)
    urizen.z = math.floor(-blocksWidth*0.5)

# For tracking subject's movement and position
# against the Perlin Noise terrain.
currentX = 0
currentZ = 0
realPosX = 0#terrainWidth*0.5
realPosZ = 0#terrainWidth*0.5

#  Let's gooooo!
generateChunk(currentX,currentZ)

# Can we save the terrain?
Mesh.save(urizen.model, 'urizen.obj')
EditorCamera()
app.run()