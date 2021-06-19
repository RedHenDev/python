""" Perlin noise experiments """
""" 
June 14 2021 - refactoring procedural chunk generation.
June 15 2021 - exploring use of static model of terrain.
June 16 2021 - success! Ghost terrain model, with tiny
                physical terrain.
June 17 2021 refactoring and developing new 'subset' system.
June 18 2021 opened on Windows - continuing dev of subset system.
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

scene.fog_density = .04
scene.fog_color = color.rgb(0,222,200)

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.01
subject.speed = 5

#  Original position of subject etc.
subject.y = 32
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
prevX = 0
prevZ = 0

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=1988)
amp = 32
freq = 104

jojo = Entity(  model='cube',
                collider=None,
                color=color.rgba(0,101,101,64))
buildMode = -1 # Toggle with 'f'

grassTex = load_texture('grass_mono.png')

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
    if key == 'g': generateGhost()
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
    global prevX, prevZ, ghostTime, ghostDone
    if  nn.abs(nn.floor(subject.z)-nn.floor(prevZ)) >= 2 or \
        nn.abs(nn.floor(subject.x)-nn.floor(prevX)) >= 2 or \
        nn.abs(subject.x-prevX)+nn.abs(subject.z-prevZ) >= 2:
        prevX = subject.x
        prevZ = subject.z
        generateShell()
    
    if buildMode==1:
        projectBuilder()
    else: jojo.y = -99 # Hide jojo.

    # Continue to build 10K terrain!
    if ghostDone == False and time.time() - ghostTime > 2:
        # subject.gravity = 0 # Prevent subject glitching through terrain.
        # subject.y += 0.2
        generateSubset()
        # subject.gravity = 0.5
        ghostTime = time.time() # Update timeStamp AFTER generation!


terrainWidth = 100
# Ghost-terrain. Parent to subets.
ghost = Entity(model=None,collider=None)

# Our physical terrain object. Parent to blocks.
shell = Entity()
shell.visible = False
shell.texture = 'grass_14.png'

# Generate pool of cubes for urizen shell.
blocks = []
blocksWidth = 5
for i in range(blocksWidth*blocksWidth):
    bub = Entity(model='cube',texture='grass_14.png',
    collider=None,parent = shell)
    bub.x = nn.floor(i/blocksWidth)
    bub.z = nn.floor(i%blocksWidth)
    bub.disable()
    blocks.append(bub)

# Cubes to populate each subset.
gblocks = []
subWidth = 50
for i in range(subWidth):
    bud = Entity(model='cube',collider=None,
            visible=False)
    bub.disable()
    gblocks.append(bud)
# Empty entity for each subset-gblocks combine.
# In turn, all subsets combined into ghost at end of process.
subsets = []
si = 0 # Current subset index. As we work across terrain.
for i in range(int((terrainWidth*terrainWidth)/subWidth)):
    bud = Entity(model=None,collider=None,
            visible=False,parent=ghost)
    bub.disable()
    subsets.append(bud)

# Combine all subsets.
def generateGhost():
    global ghostDone
    ghost.combine(auto_destroy=True)
    ghost.texture='grass_mono.png'
    ghost.color=color.rgb(222,0,0)
    ghost.collider=None
    ghostDone = True
    

# Terrain data.
urizenData = []
for i in range (terrainWidth*terrainWidth):
    # NB. This was reversed in previous non-subset version.
    x = nn.floor(i/terrainWidth)
    z = nn.floor(i%terrainWidth)
    # freq = 64
    # amp = 12
    y = (noise([x/freq,z/freq])* amp)
    y = nn.floor(y)
    urizenData.append(y)

def generateShell():
    global terrainWidth, blocksWidth
    for i in range(blocksWidth*blocksWidth):
        x = nn.floor(nn.floor(subject.x) + (i/blocksWidth))
        z = nn.floor(nn.floor(subject.z) + (i%blocksWidth))
        # Check index. If out of range, return to default
        # shell position.
        indi = int((x*terrainWidth)+z)
        
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                y = blocks[i].y = -7
        else: y = blocks[i].y = urizenData[indi]

    shell.model = None
    shell.combine(auto_destroy=False)
    shell.collider = 'mesh'
    # Centre subject relative to shell.
    shell.x = nn.floor(subject.x + -((blocksWidth-2.5)*0.5))
    shell.z = nn.floor(subject.z + -((blocksWidth-2.5)*0.5))

gbi = 0 # Current index. I.e., of created ghostblock so far.
ghostTime = 0 # Time stamp for when to generate new subset.
ghostDone = False
def generateSubset():
    global gbi, si, terrainWidth, subWidth, ghostDone
    # Safety catch...
    if gbi >= len(urizenData)-1: 
        if ghostDone == False:
            generateGhost()
        return
    # Iterate from current index to index + (subWidth-1).
    # Currently, a strip of 50...
    for i in range(gbi,gbi+subWidth):
        x = gblocks[i-gbi].x = nn.floor(i/terrainWidth)
        z = gblocks[i-gbi].z = nn.floor(i%terrainWidth)
        # Check index. If out of range, return to default
        # subset position. NB Not sure we need this anymore?
        indi = int((x*terrainWidth)+z)
        
        gblocks[i-gbi].y = urizenData[indi]
        # nn.floor(noise([x/freq,z/freq])* amp)
        gblocks[i-gbi].collider=None
        gblocks[i-gbi].parent=subsets[si]
        gblocks[i-gbi].disable()
    
    # If finished all subsets...
    # First combine gblocks into this final
    # subset, then signal to generate combined ghost.
    if gbi >= len(urizenData)-1:
        subsets[si].combine(auto_destroy=True) 
        generateGhost()
    else: 
        subsets[si].combine(auto_destroy=False)
        gbi += subWidth # Increment to new ghost block index.
        si += 1        # Increment to next subset index.
        subsets[si].collider=None
        subsets[si].visible = True
        subsets[si].texture = grassTex
        subsets[si].color = color.rgb(200,0,0)

#  Let's gooooo!
generateShell()

app.run()