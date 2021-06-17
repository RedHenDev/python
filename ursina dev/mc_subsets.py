""" Perlin noise experiments """
""" 
June 14 2021 - refactoring procedural chunk generation.
June 15 2021 - exploring use of static model of terrain.
June 16 2021 - success! Ghost terrain model, with tiny
                physical terrain.
June 17 2021 refactoring and developing new 'subset' system.
"""

from ursina import * 
import numpy as nn
import random as ra
import math
import time

from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=1988)

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
    global prevX, prevZ
    if  nn.abs(math.floor(subject.z)-math.floor(prevZ)) >= 2 or \
        nn.abs(math.floor(subject.x)-math.floor(prevX)) >= 2 or \
        nn.abs(subject.x-subject.x)+nn.abs(subject.z-subject.z) >= 2:
        prevX = subject.x
        prevZ = subject.z
        generateShell()
    
    if buildMode==1:
        projectBuilder()
    else: jojo.y = -99 # Hide jojo.



# Our physical terrain object. Parent to blocks.
shell = Entity()
# urizen.visible=False
shell.texture = 'grass_14.png'

# Generate pool of blocks. Also decide colours here.
blocks = []
blocksWidth = 5
for i in range(blocksWidth*blocksWidth):
    bub = Entity(model='cube',texture='grass_14.png')
    bub.x = math.floor(i/blocksWidth)
    bub.z = math.floor(i%blocksWidth)
    bub.parent = shell
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

def generateShell():
    global terrainWidth, blocksWidth
    shell.model=None
    for i in range(blocksWidth*blocksWidth):
        x = nn.floor(nn.floor(subject.x) + (i/blocksWidth))
        z = nn.floor(nn.floor(subject.z) + (i%blocksWidth))
        # Check index. If out of range, return to default
        # chunk position.
        indi = int((x*terrainWidth)+z)
        
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                y = blocks[i].y = -7
        else: y = blocks[i].y = urizenData[indi]

    shell.combine(auto_destroy=False)
    shell.collider = 'mesh'
    # Centre subject relative to chunk.
    shell.x = math.floor(subject.x + -((blocksWidth-2.5)*0.5))
    shell.z = math.floor(subject.z + -((blocksWidth-2.5)*0.5))

scene.fog_density = .04
scene.fog_color = color.rgb(0,222,200)
subject = FirstPersonController()
subject.gravity = 0.5
subject.speed = 6

#  Original position of subject etc.
subject.y = 6
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
prevX = 0
prevZ = 0

#  Let's gooooo!
generateShell()

# Ghost-terrain.
ghost = Entity( model=None,
            texture='grass_14.png',
            color=color.rgb(0,255,0),
            collider=None)

ci = 0
def generateGhost(_ci):
    global ci
    if ci >= len(urizenData): return
    global terrainWidth, blocksWidth
    for i in range(ci,ci+blocksWidth):
        x = nn.floor(nn.floor(subject.x) + (i/blocksWidth))
        z = nn.floor(nn.floor(subject.z) + (i%blocksWidth))
        # Check index. If out of range, return to default
        # chunk position.
        indi = int((x*terrainWidth)+z)
        
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                y = blocks[i].y = -7
        else: y = blocks[i].y = urizenData[indi]

    shell.combine(auto_destroy=False)
    shell.collider = 'mesh'
    # Centre subject relative to chunk.
    shell.x = math.floor(subject.x + -((blocksWidth-2.5)*0.5))
    shell.z = math.floor(subject.z + -((blocksWidth-2.5)*0.5))

subject.cursor.visible = False

app.run()