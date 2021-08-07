""" Perlin noise experiments """
""" 
June 14 2021 - refactoring procedural chunk generation.
June 15 2021 - exploring use of static model of terrain.
June 16 2021 - success! Ghost terrain model, with tiny
                physical terrain.
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

sunY = 0

jojo = Entity(  model='cube',
                collider=None,
                color=color.rgba(0,101,101,64))
buildMode = 1 # Toggle with 'f'

def projectBuilder():
    jojo.position = subject.position + Vec3(camera.forward * 2)
    jojo.x = nn.round(jojo.x)
    jojo.y = nn.round(jojo.y)
    jojo.z = nn.round(jojo.z)
    jojo.y+=2

def input(key):
    global buildMode
    if key == 'q' or key == 'escape': 
        exit()
    if key == 'f': 
        buildMode *= -1 # Toggle build mode.     
    if key == 'left mouse up' and buildMode==1:
        projectBuilder()
        e = duplicate(jojo)
        e.collider = 'box'
        e.color=color.white
        e.texture='grass_mono.png'
        e.shake(duration=0.5,speed=0.01)
    elif key == 'right mouse up' and buildMode==1:
        e = mouse.hovered_entity
        if e and e.visible==True:
            destroy(e)

def update():
    global sunY
    global currentX, currentZ
    if  nn.abs(math.floor(subject.z)-math.floor(currentZ)) >= 2 or \
        nn.abs(math.floor(subject.x)-math.floor(currentX)) >= 2 or \
        nn.abs(subject.x-subject.x)+nn.abs(subject.z-subject.z) >= 2:
        currentX = subject.x
        currentZ = subject.z
        generateChunk()
    
    if buildMode==1:
        projectBuilder()
    else: jojo.y = -99 # Hide jojo.

    sun.rotation_y += 10 * time.dt
    sunY += 0.01
    sun.y += (nn.sin(sunY) * 2.8) * time.dt

class Block:
    def __init__(this):
        this.ent = Entity(model="cube",
                          texture='grass_14.png')

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

sun = Entity(model="cube",color=color.rgba(222,200,0,200),
                scale=24,
                texture='2k_sun')
sun.y = 64
sun.x = 64
sun.z = 64

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=1988)

# Our physical terrain object. Parent to blocks.
urizen = Entity()
# urizen.visible=False
urizen.texture = 'grass_14.png'

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 5
for i in range(blocksWidth*blocksWidth):
    bub = Block()
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
                y = blocks[i].ent.y = -7
        else: y = blocks[i].ent.y = urizenData[indi]
        # blocks[i].ent.disable() # NB don't have to enable blocks.
        # Decide colour of each block according to height.
        # r = 160 + y * 10
        # g = 160 + y * 42
        # b = 0
        # blocks[i].ent.color=color.rgb(r,g,b)

    urizen.combine(auto_destroy=False)
    urizen.collider = 'mesh'
    # Centre subject relative to chunk.
    urizen.x = math.floor(subject.x + -((blocksWidth-2.5)*0.5))
    urizen.z = math.floor(subject.z + -((blocksWidth-2.5)*0.5))

scene.fog_density = .04
scene.fog_color = color.rgb(0,222,200)
subject = FirstPersonController()
subject.gravity = 0.5
subject.speed = 6

#  Original position of subject etc.
subject.y = 6
subject.x = 50
subject.z = 50

# For tracking subject's movement and position
# against the Perlin Noise terrain.
currentX = 0
currentZ = 0

# Infinite-plane.
ip = Entity(model='quad',position=Vec3(-10000,-7,-10000),
        rotation_x=90,
        scale=30000,color=rgb(100,0,0))

#  Let's gooooo!
generateChunk()

# Ghost-terrain.
mo = load_model('i') 
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

subject.cursor.visible = False
subject.gravity = 0
app.run()
