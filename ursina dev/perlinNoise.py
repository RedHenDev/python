""" Perlin noise experiments """

from ursina import *
import numpy as nn
import random as ra
import math

#from pnoise import pnoise2
from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController
#from ursina.shaders import lit_with_shadows_shader

sunY = 0

def input(key):
    global currentZ,currentX
    if key == 'q' or key == 'escape': 
        locked = False
        exit()
    if key == 'g':
        currentZ += subject.z-blocksWidth*0.5
        currentX += subject.x-blocksWidth*0.5
        generateChunk(  currentX,
                        currentZ)
        # Adjust subject a little higher to
        # prevent falling through new chunk. 
        subject.y += 0.1
        # Return subject to starting position.
        urizen.z -= subject.z-blocksWidth*0.5
        subject.z = blocksWidth*0.5
        urizen.x -= subject.x-blocksWidth*0.5
        subject.x = blocksWidth*0.5
        

def update():
    global sunY
    print_on_screen('x='+str(math.floor(subject.x))
                        +'\nz='+str(math.floor(subject.z)))
    sun.rotation_y += 10 * time.dt
    sunY += 0.01
    sun.y += (nn.sin(sunY) * 2.8) * time.dt
    #for b in blocks:
    #    b.update() # For highlighting when hovered.

class Block:
    def __init__(this, _scale):
        this.ent = Entity(model="cube",color=color.white,
                          scale=_scale,texture='grass_12.png')
        this.origColor = this.ent.color

    def update(this):
        if this.ent.hovered:
            this.ent.color = color.lime
        else: this.ent.color = this.origColor

app = Ursina()

window.color = color.rgb(0,111,184)

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),
                scale=12,
                texture='2k_sun')
sun.y = 22
sun.x = 2222
sun.z = 2222

# Perlin noise setup.
noise = PerlinNoise(octaves=3,seed=1)

# Our terrain object.
urizen = Entity()

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 10
for i in range(blocksWidth*blocksWidth):
    bub = Block(1)
    whatShade = ra.randint(100,122)
    bub.ent.color=color.rgb(0,whatShade,0)
    bub.origColor = bub.ent.color
    bub.ent.parent = urizen
    blocks.append(bub)

# Seed origin -- also where subject begins.
seedX = 0
seedZ = 0
# For tracking subject's movement and position.
deltaX = 0
deltaZ = 0
currentX = seedX
currentZ = seedZ

# Terrain data.
urizenData = []
terrainWidth = 100
for i in range (terrainWidth*terrainWidth): 
    x = math.floor(i/terrainWidth)
    z = math.floor(i%terrainWidth)
    freq = 64
    amp = 12
    y = (noise([x/freq,z/freq])* amp)
    urizenData.append(math.floor(y))

def generateChunk(_ox, _oz):
    global terrainWidth
    global blocksWidth
    urizen.model=None
    for i in range(blocksWidth*blocksWidth):
        blocks[i].ent.x =    math.floor(_ox + 
                             math.floor(i/blocksWidth))
        blocks[i].ent.z =    math.floor(_oz + 
                             math.floor(i%blocksWidth))
        x = blocks[i].ent.x
        z = blocks[i].ent.z
        blocks[i].ent.y =   urizenData[int(((x-seedX)*
                            terrainWidth)+z-seedZ)]
    
    for b in blocks:
        b.ent.enable()
    urizen.combine(auto_destroy=False)
    for b in blocks:
        b.ent.disable()
    urizen.collider = 'mesh'
    urizen.texture = 'grass_14.png'
    

generateChunk(seedX,seedZ)

"""
for i in range(100):
    bub = Block(1)
    whatShade = ra.randint(100,122)
    bub.ent.color=color.rgb(whatShade,
    whatShade,whatShade)
    bub.origColor = bub.ent.color
    bub.ent.x = 1984 + math.floor(i/10)
    bub.ent.z = 1984 + math.floor(i % 10)
    freq = 64
    amp = 12
    #bub.ent.scale_y = 10
    #bub.ent.y = math.floor(noise([bub.ent.x/freq,bub.ent.z/freq])* amp)
    bub.ent.y = urizenData[int(((bub.ent.x-1984)*500)+
    bub.ent.z-1984)]
    #bub.ent.collider='cube'
    bub.ent.parent = urizen
    
    #destroy(bub.ent)
    #blocks.append(bub)

urizen.combine()
urizen.collider = 'mesh'
urizen.texture = 'grass_14.png'
"""

scene.fog_density = .03
scene.fog_color = color.rgb(0,111,184)
subject = FirstPersonController(model='cube')
subject.gravity = 0.5
subject.y = 32
subject.x = 5
subject.z = 5
app.run()