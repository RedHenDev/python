"""
June 19 2021 Mac -- meta subset system begun. Working!
"""

from ursina import * 
import numpy as nn
import time

from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False

scene.fog_density = .02
scene.fog_color = color.rgb(0,222,200)

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.speed = 6

#  Original position of subject etc.
subject.y = 12
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
prevX = 0
prevZ = 0

# Perlin noise setup.
noise = PerlinNoise(octaves=10,seed=99)
amp = 12
freq = 64
terrainDepth = 7

jojo = Entity(  model='cube',
                collider=None,
                color=color.rgba(0,101,101,64))
buildMode = -1 # Toggle with 'f'

grassTex = load_texture('grass_mono.png')
patternTex = load_texture('grass_14.png')

def projectBuilder():
    jojo.position = (subject.position +
     Vec3(camera.forward * 2))
    jojo.x = nn.round(jojo.x)
    jojo.y = nn.floor(jojo.y)
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
        e.texture=grassTex
        e.color=color.white
        e.shake(duration=0.5,speed=0.01)
    elif key == 'right mouse up' and buildMode==1:
        e = mouse.hovered_entity
        if e and e.visible==True:
            destroy(e)

def update():
    global prevX, prevZ, ghostTime, ghostDone
    if  nn.abs(nn.floor(subject.z)-nn.floor(prevZ)) >= 1 or \
        nn.abs(nn.floor(subject.x)-nn.floor(prevX)) >= 1 or \
        nn.abs(subject.x-prevX)+nn.abs(subject.z-prevZ) >= 1:
        prevX = subject.x
        prevZ = subject.z
        generateShell()
    
    if buildMode==1:
        projectBuilder()
    else: jojo.y = -9999 # Hide jojo.

    # Continue to build 10K terrain!
    if ghostDone == False and time.time() - ghostTime > 0.5:
        generateSubset()
        # Update timeStamp AFTER generation of subset!
        ghostTime = time.time() 

terrainWidth = 100
# Ghost-terrain. Parent to subets.
ghost = Entity(model=None,collider=None)

# Our physical terrain object. Parent to blocks.
shell = Entity(model=None,collider=None)
shell.visible = False

# Generate pool of cubes for urizen shell.
blocks = []
blocksWidth = 5
for i in range(blocksWidth*blocksWidth):
    bub = Entity(model='cube',
    collider=None,parent=shell,visible=False)
    bub.disable()
    blocks.append(bub)

# Cubes to populate each subset.
gblocks = []
subWidth = terrainWidth
for i in range(subWidth*terrainDepth):
    bud = Entity(model='cube',collider=None,
            visible=False,scale_y=terrainDepth)
    bub.disable()
    gblocks.append(bud)
# Empty entity for each subset-gblocks combine.
# In turn, all subsets combined into ghost at end of process.
subsets = []
si = 0 # Current subset index. As we work across terrain.
subsDone = False
totNumSubs = int((terrainWidth*terrainWidth)/subWidth)
for i in range(totNumSubs):
    bud = Entity(model=None,collider=None,
            visible=False)
    bud.parent=ghost
    bub.disable()
    subsets.append(bud)

# Combine all subsets.
def generateGhost():
    global ghostDone
    subject.y += 12 # Prevent fall glitch.
    subject.gravity = 0
    ghost.combine(auto_destroy=True)
    ghost.texture=grassTex
    ghost.color=color.rgb(200,20,20)
    ghost.collider=None
    ghostDone=True
    subject.gravity = 0.5
    

# Terrain data.
urizenData = []
for i in range (terrainWidth*terrainWidth):
    # NB. This was reversed in previous non-subset version.
    x = nn.floor(i/terrainWidth)
    z = nn.floor(i%terrainWidth)
    y = (noise([x/freq,z/freq])* amp)
    y = nn.floor(y)
    urizenData.append(y)

def generateShell():
    global terrainWidth, blocksWidth
    for i in range(blocksWidth*blocksWidth):
        x = blocks[i].x = nn.floor(subject.x + (i/blocksWidth))
        z = blocks[i].z = nn.floor(subject.z +
        (i%blocksWidth))
        # Check index. If out of range, return to default
        # shell position.
        indi = int((x*terrainWidth)+z)
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                blocks[i].y = -7
        else:   blocks[i].y = nn.floor(urizenData[indi]+(terrainDepth*0.5))

    shell.model = None
    shell.combine(auto_destroy=False)
    shell.collider = 'mesh'
    # shell.texture = patternTex
    # shell.visible = True

gbi = 0 # Current index. I.e., of created ghostblock so far.
ghostTime = 0 # Time stamp for when to generate new subset.
ghostDone = False
def generateSubset():
    global gbi, si, terrainWidth, subWidth, subsDone, ghostDone
    global totNumSubs
    # Safety catches...
    if subsDone: return
    if gbi >= len(urizenData)-1: 
        if ghostDone == False:
            generateGhost()
        return
    # Iterate from current index to index + (subWidth-1).
    # Currently, a strip of 100...
    for i in range(gbi,gbi+subWidth):
        x = gblocks[i-gbi].x = nn.floor(i/terrainWidth)
        z = gblocks[i-gbi].z = nn.floor(i%terrainWidth)
        # Check index. If out of range, return to default
        # subset position. NB Not sure we need this anymore?
        indi = int((x*terrainWidth)+z)
        # I could iterate here for layers...
        gblocks[i-gbi].y = urizenData[indi]
        # nn.floor(noise([x/freq,z/freq])* amp)
        gblocks[i-gbi].collider=None
        gblocks[i-gbi].parent=subsets[si]
        gblocks[i-gbi].disable()
    
    # If finished all subsets...
    # First combine gblocks into this final
    # subset, then signal to generate combined ghost.
    # Else combine without destroying and
    # increment si and gbi for next subset.
    if gbi >= len(urizenData)-1:
        subsets[si].combine(auto_destroy=True)
        subsDone = True 
        generateGhost()
    else: 
        subsets[si].combine(auto_destroy=False)
        gbi += subWidth # Increment to new ghost block index.
        subsets[si].collider = None
        subsets[si].visible = True
        subsets[si].texture = grassTex
        subsets[si].color = color.rgb(111,0,0)
        if si >= totNumSubs: subsDone = True
        else: si += 1        # Increment to next subset index.

#  Let's gooooo!
generateShell()

app.run()