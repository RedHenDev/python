""" Perlin noise experiments """
""" 
June 14 2021 - refactoring procedural chunk generation.
June 15 2021 - exploring use of static model of terrain.
"""

from ursina import *
# from ursina.mesh_importer import *
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
    if key == 'q' or key == 'escape': 
        exit()
    if key == 'g':
        updateTerrain()

def updateTerrain():
    # Return subject to starting position.
    # subject.z = 0
    # subject.x = 0
    generateChunk()
    # adjustGhostTerrain() 
    

def adjustGhostTerrain():
    pass
    #  Adjust ghost-terrain.
    a.z += (-currentZ*0.5)
    a.x += (-currentX*0.5)
    # Adjust for subject centrality on urizen.
    a.x += blocksWidth*0.5
    a.z += -blocksWidth*0.5

def update():
    global sunY
    global currentX, currentZ
    if  nn.abs(math.floor(subject.z)-math.floor(currentZ)) >= 1 or \
        nn.abs(math.floor(subject.x)-math.floor(currentX)) >= 1 or \
        nn.abs(subject.x-subject.x)+nn.abs(subject.z-subject.z) >= 1:
    # if  nn.abs(subject.z) >= 1 or nn.abs(subject.x) >= 1:
        pass
        currentX = subject.x
        currentZ = subject.z
        updateTerrain()
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
urizen.texture = 'grass_mono.png'

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 5
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
    # NB. I have reversed the x and z here, to fit
    # ghost-model. 
    x = math.floor(i%terrainWidth)
    z = math.floor(i/terrainWidth)
    freq = 64
    amp = 12
    y = (noise([x/freq,z/freq])* amp)
    y = math.floor(y)
    urizenData.append(y)

def generateChunk():
    global terrainWidth, blocksWidth
    urizen.model=None
    for i in range(blocksWidth*blocksWidth):
        x = math.floor(nn.floor(subject.x) + (i/blocksWidth))
        z = math.floor(nn.floor(subject.z) + (i%blocksWidth))
        # Check index. If out of range, return to default
        # chunk position.
        indi = int((x*terrainWidth)+z)
        
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                y = blocks[i].ent.y = -4
        else: y = blocks[i].ent.y = urizenData[indi]

        # Decide colour of each block according to height.
        r = 160 + y * 10
        g = 160 + y * 42
        b = 0
        blocks[i].ent.color=color.rgb(r,g,b)
        # blocks[i].ent.color=color.black66

    for b in blocks:
        b.ent.enable()
    urizen.combine(auto_destroy=False)
    for b in blocks:
        b.ent.disable()
    urizen.collider = 'mesh'
    # urizen.collider = None # For testing...
    # Centre subject relative to chunk.
    urizen.x = math.floor(subject.x + -((blocksWidth-2.5)*0.5))
    urizen.z = math.floor(subject.z + -((blocksWidth-2.5)*0.5))

scene.fog_density = .04
scene.fog_color = color.rgb(0,211,184)
subject = FirstPersonController()
subject.gravity = 1
subject.speed = 6

#  Original position of subject etc.
subject.y = 6
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
currentX = 0
currentZ = 0

# Infinite-plane.
ip = Entity(model='quad',position=Vec3(-10000,-6,-10000),
        rotation_x=90,
        scale=30000,color=rgb(100,0,0))

#  Let's gooooo!
generateChunk()

# Ghost-terrain.
mo = load_model('france.obj') 
a = Entity( model=mo,
            texture='grass_14.png',
            color=color.rgb(0,255,0),
            double_sided = True)
# Adjust position of ghost-terrain to correspond to
# smaller terrain's collider.
a.x = math.floor(a.x)
a.z = math.floor(a.z)
a.rotation_y=90
# # Adjust for subject centrality on urizen.
a.x += 8.39
a.z -= 2
"""
sf = sun.add_script(SmoothFollow(
    target=subject, offset=(0,2,0),speed=0.1))
"""
# Can we save the terrain?
# Mesh.save(urizen.model, 'urizen2.obj')

app.run()