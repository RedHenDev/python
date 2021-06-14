""" Perlin noise experiments """
""" 
June 14 2021 - refactoring procedural chunk generation.
"""

from ursina import *
import numpy as nn
import random as ra
import math
import time

#from pnoise import pnoise2
from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController
#from ursina.shaders import lit_with_shadows_shader

sunY = 0

def input(key):
    global currentZ,currentX
    if key == 'q' or key == 'escape': 
        exit()
    if key == 'g':
        updateTerrain()
    if  nn.abs(subject.z) >= math.floor(blocksWidth*0.25) or \
        nn.abs(subject.x) >= math.floor(blocksWidth*0.25):
        updateTerrain()

def updateTerrain():
    global currentZ,currentX
    currentZ += subject.z
    currentX += subject.x
    # Adjust subject a little higher to
    # prevent falling through new chunk. 
    subject.y += 0.2
    # Return subject to starting position.
    subject.z = 0
    subject.x = 0
    generateChunk(  currentX,
                    currentZ)

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
                          scale=_scale,texture='grass_mono.png')
        this.origColor = this.ent.color

    def update(this):
        if this.ent.hovered:
            this.ent.color = color.lime
        else: this.ent.color = this.origColor

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),
                scale=12,
                texture='2k_sun')
sun.y = 22
sun.x = 22
sun.z = 22

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=1988)

# Our terrain object.
urizen = Entity()

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 20
for i in range(blocksWidth*blocksWidth):
    bub = Block(1)
    bub.ent.scale_y = 6
    bub.ent.x = math.floor(i/blocksWidth)
    bub.ent.z = math.floor(i%blocksWidth)
    bub.ent.parent = urizen
    blocks.append(bub)

# Terrain data.
urizenData = []
terrainWidth = 20
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

scene.fog_density = .01
scene.fog_color = color.rgb(0,211,184)
subject = FirstPersonController()
subject.gravity = 0.5

#  Original position of subject etc.
subject.y = 12
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
currentX = 0
currentZ = 0
realPosX = 0#terrainWidth*0.5
realPosZ = 0#terrainWidth*0.5

#  Let's gooooo!
generateChunk(currentX,currentZ)
"""
sf = sun.add_script(SmoothFollow(
    target=subject, offset=(0,2,0),speed=0.1))
"""
# Can we save the terrain?
Mesh.save(urizen, 'urizen')

app.run()